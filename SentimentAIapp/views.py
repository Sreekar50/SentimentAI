from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import Comment, AnalysisHistory
import tweepy
import instaloader
import time
import spacy
import torch
import re
import json
from bs4 import BeautifulSoup
from transformers import BertForSequenceClassification, BertTokenizer
from googleapiclient.discovery import build
from collections import Counter
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import logging
from .auth import get_user_from_token  
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Spacy model loaded successfully")
except Exception as e:
    logger.error(f"Error loading spacy: {e}")
    nlp = None

try:
    bert_model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    bert_tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    logger.info("BERT model loaded successfully")
except Exception as e:
    logger.error(f"Error loading BERT: {e}")
    bert_model = None
    bert_tokenizer = None

L = instaloader.Instaloader()


USERNAME = ""
PASSWORD = ""

try:
    L.load_session_from_file(USERNAME)
except FileNotFoundError:
    L.login(USERNAME, PASSWORD)
    L.save_session_to_file()
    
def calculate_trend_score(sentiments):
    positive = sentiments.count('POSITIVE')
    negative = sentiments.count('NEGATIVE')
    total = len(sentiments)
    return round((positive / total) * 100, 2) if total > 0 else 0

@csrf_exempt
@api_view(['POST', 'GET'])
def fetch_comments(request):
    logger.info(f"Received {request.method} request to fetch_comments")
    logger.info(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
    
    user = get_user_from_token(request)
    if not user:
        logger.warning("User not authenticated via token")
        return Response({
            'error': 'Authentication required. Please login first.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    logger.info(f"User authenticated via token: {user.username}")
    
    if request.method == 'GET':  
        logger.info("GET request - returning test message")
        return Response({
            "message": "API is working! Use POST to fetch comments.",
            "user": user.username
        })
    
    try:
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request data: {request.data}")
        
        url = request.data.get('url')
        
        logger.info(f"Extracted URL: {url}")
        
        if not url:
            return Response({
                'error': 'URL is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info("Starting comment scraping...")
        
        comments_data = scrape_comments(url)
        # logger.info(f"Scraped comments: {comments_data}")
        
        if isinstance(comments_data, dict) and 'error' in comments_data:
            return Response(comments_data, status=status.HTTP_400_BAD_REQUEST)
        
        insights = analyze_comments(comments_data, url, user)
        # logger.info(f"Analysis results: {insights}")
        return Response(insights)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Response({
            'error': f'Analysis failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API credentials (Replace with your own)
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_SECRET = ""

# Authenticate Twitter API
try:
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    twitter_api = tweepy.API(auth)
    logger.info("Twitter API authenticated successfully")
except Exception as e:
    logger.error(f"Twitter API authentication failed: {e}")
    twitter_api = None

# YouTube API Key (Replace with your own)
YOUTUBE_API_KEY = ""
try:
    youtube_api = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    logger.info("YouTube API authenticated successfully")
except Exception as e:
    logger.error(f"YouTube API authentication failed: {e}")
    youtube_api = None

def scrape_comments(url):
    logger.info(f"Scraping comments from URL: {url}")
    comments = []

    if "twitter.com" in url:
        comments = fetch_twitter_replies(url)
        platform = "Twitter"

    elif "instagram.com" in url:
        result = fetch_instagram_comments(url)
        if isinstance(result, dict) and 'error' in result:
            return result
        comments = result.get('comments', [])
        platform = "Instagram"

    elif "youtube.com" in url or "youtu.be" in url:
        comments = fetch_youtube_comments(url)
        platform = "YouTube"

    elif "amazon." in url or "flipkart." in url:
        comments = fetch_ecommerce_reviews(url)
        platform = "E-commerce"
    else:
        return {'error': 'Unsupported platform'}

    logger.info(f"Platform: {platform}, Comments found: {len(comments)}")
    return {
        'comments': comments,
        'platform': platform
    }

def fetch_twitter_replies(url):
    comments = []
    try:
        tweet_id = url.split("/")[-1].split("?")[0]
        replies = tweepy.Cursor(twitter_api.search_tweets, q=f"to:{tweet_id}", tweet_mode='extended').items(50)
        comments = [reply.full_text for reply in replies if not reply.full_text.startswith('RT')]
    except Exception as e:
        print("Error fetching Twitter comments:", e)
    return comments

def fetch_instagram_comments(url):
    match = re.search(r"(?:p|reel)/([^/?]+)", url)
    if not match:
        return {"error": "Invalid Instagram URL"}
    shortcode = match.group(1)
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = []
        for comment in post.get_comments():
            comments.append(comment.text)
        if not comments:
            return {"error": "No comments found"}
        return {"comments": comments}
    except Exception as e:
        return {"error": f"Error fetching comments: {str(e)}"}

def fetch_youtube_comments(url):
    comments = []
    try:
        video_id_match = re.search(r"v=([^&]+)", url) or re.search(r"youtu\.be/([^/?]+)", url)
        if video_id_match:
            video_id = video_id_match.group(1)
            response = youtube_api.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            ).execute()

            for item in response.get("items", []):
                comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
    except Exception as e:
        print("Error fetching YouTube comments:", e)
    return comments

def fetch_ecommerce_reviews(url):
    comments = []
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        if "amazon." in url:
            reviews = soup.find_all("span", {"data-hook": "review-body"})
        elif "flipkart." in url:
            reviews = soup.find_all("div", {"class": "t-ZTKy"})
        comments = [review.get_text(strip=True) for review in reviews[:50]]
    except Exception as e:
        print("Error fetching e-commerce reviews:", e)
    return comments

def analyze_comments(comments_data, url, user):
    logger.info("Starting comment analysis...")
    
    comments = comments_data.get('comments', [])
    platform = comments_data.get('platform', 'Unknown')
    
    if not comments: 
        logger.warning("No comments found to analyze")
        return {
            "positive_percent": 0, 
            "negative_percent": 0, 
            "neutral_percent": 0, 
            "purchase_intent_percent": 0,
            "total_comments": 0,
            "platform": platform
        }
    
    sentiments = []
    purchase_intent_count = 0
    purchase_words = ['buy', 'purchase', 'order', 'cart', 'checkout', 'will order', 'want to buy']
    
    for comment in comments:
        try:
            inputs = bert_tokenizer(comment, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = bert_model(**inputs)
            sentiment_score = torch.argmax(outputs.logits, axis=1).item()
            sentiment = 'POSITIVE' if sentiment_score > 3 else 'NEGATIVE'
            if 'buy' in comment.lower() or 'purchase' in comment.lower():
                purchase_intent_count += 1
            sentiments.append(sentiment)
            
            try:
                Comment.objects.create(
                    platform=platform,
                    content=comment,
                    sentiment=sentiment,
                    purchase_intent=any(word in comment.lower() for word in purchase_words),
                    user=user
                )
            except Exception as db_error:
                logger.error(f"Database save error: {db_error}")
            
        except Exception as e:
            logger.error(f"Error analyzing comment: {e}")
            continue

    total_comments = len(comments)
    positive_count = sentiments.count('POSITIVE')
    negative_count = sentiments.count('NEGATIVE')
    neutral_count = sentiments.count('NEUTRAL')
    
    positive_percent = round((positive_count / total_comments) * 100, 2)
    negative_percent = round((negative_count / total_comments) * 100, 2)
    neutral_percent = round((neutral_count / total_comments) * 100, 2)
    purchase_intent_percent = round((purchase_intent_count / total_comments) * 100, 2)

    try:
        AnalysisHistory.objects.create(
            user=user,
            url=url,
            platform=platform,
            positive_percent=positive_percent,
            negative_percent=negative_percent,
            purchase_intent_percent=purchase_intent_percent,
            total_comments=total_comments
        )
        logger.info("Analysis history saved successfully")
    except Exception as e:
        logger.error(f"Error saving analysis history: {e}")

    result = {
        'positive_percent': positive_percent,
        'negative_percent': negative_percent,
        'neutral_percent': neutral_percent,
        'purchase_intent_percent': purchase_intent_percent,
        'total_comments': total_comments,
        'platform': platform
    }
    
    # logger.info(f"Analysis completed: {result}")
    return result

@csrf_exempt
@api_view(['GET'])
def get_analysis_history(request):
    """Get user's analysis history"""
    user = get_user_from_token(request)
    if not user:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        history = AnalysisHistory.objects.filter(user=user).order_by('-created_at')[:10]
        history_data = []
        
        for analysis in history:
            history_data.append({
                'id': analysis.id,
                'url': analysis.url,
                'platform': analysis.platform,
                'positive_percent': analysis.positive_percent,
                'negative_percent': analysis.negative_percent,
                'purchase_intent_percent': analysis.purchase_intent_percent,
                'total_comments': analysis.total_comments,
                'created_at': analysis.created_at.isoformat()
            })
        
        return Response({'history': history_data})
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch history: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
