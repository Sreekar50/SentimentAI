from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from transformers import pipeline
from .models import Comment
import tweepy
import instaloader
import spacy
import torch
import re
import json
from bs4 import BeautifulSoup
from transformers import BertForSequenceClassification, BertTokenizer
from googleapiclient.discovery import build
from collections import Counter
import pandas as pd

nlp = spacy.load("en_core_web_sm")
bert_model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
bert_tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# # Twitter API setup
# twitter_auth = tweepy.OAuth1UserHandler('YOUR_API_KEY', 'YOUR_API_SECRET', 'YOUR_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN_SECRET')
# twitter_api = tweepy.API(twitter_auth)

def calculate_trend_score(sentiments):
    positive = sentiments.count('POSITIVE')
    negative = sentiments.count('NEGATIVE')
    total = len(sentiments)
    return round((positive / total) * 100, 2) if total > 0 else 0

@api_view(['POST','GET'])
def fetch_comments(request):
    if request.method == 'GET':  
        return Response({"message": "API is working! Use POST to fetch comments."})
    url = request.data.get('url')
    comments = scrape_comments(url)
    insights = analyze_comments(comments)
    return Response(insights)


TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_SECRET = ""


auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)


YOUTUBE_API_KEY = ""
youtube_api = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def scrape_comments(url):
    comments = []

    if "twitter.com" in url:
        comments = fetch_twitter_replies(url)

    elif "instagram.com" in url:
        comments = fetch_instagram_comments(url)

    elif "youtube.com" in url or "youtu.be" in url:
        comments = fetch_youtube_comments(url)

    elif "amazon." in url or "flipkart." in url:
        comments = fetch_ecommerce_reviews(url)

    return comments

def fetch_twitter_replies(url):
    comments = []
    try:
        tweet_id = url.split("/")[-1].split("?")[0]
        replies = tweepy.Cursor(twitter_api.search_tweets, q=f"to:{tweet_id}", tweet_mode='extended').items(50)
        comments = [reply.full_text for reply in replies if not reply.full_text.startswith('RT')]
    except Exception as e:
        print("Error fetching Twitter comments:", e)
    return comments

import instaloader
import time

L = instaloader.Instaloader()


USERNAME = ""
PASSWORD = ""


try:
    L.load_session_from_file(USERNAME)
except FileNotFoundError:
    L.login(USERNAME, PASSWORD)
    L.save_session_to_file()

def fetch_instagram_comments(url):
    """Fetch comments from Instagram posts & reels using Instaloader."""
    
    
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


def analyze_comments(comments):
    insights = []
    sentiments = []
    purchase_intent_count = 0
    if not comments:  
        return {"positive": 0, "negative": 0, "neutral": 0}
    for comment in comments:
        inputs = bert_tokenizer(comment, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = bert_model(**inputs)
        sentiment_score = torch.argmax(outputs.logits, axis=1).item()
        sentiment = 'POSITIVE' if sentiment_score > 3 else 'NEGATIVE'
        if 'buy' in comment.lower() or 'purchase' in comment.lower():
            purchase_intent_count += 1
        sentiments.append(sentiment)

    total_comments = len(comments)
    # print(comments)
    print(total_comments)
    positive_percent = round((sentiments.count('POSITIVE') / total_comments) * 100, 2)
    negative_percent = round((sentiments.count('NEGATIVE') / total_comments) * 100, 2)
    purchase_intent_percent = round((purchase_intent_count / total_comments) * 100, 2)

    return {
        'positive_percent': positive_percent,
        'negative_percent': negative_percent,
        'purchase_intent_percent': purchase_intent_percent
    }
    
