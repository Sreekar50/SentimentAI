# Social Media Sentiment Analysis Platform

A comprehensive web application that analyzes sentiment and purchase intent from comments and reviews across multiple social media and e-commerce platforms including Twitter, Instagram, YouTube, Amazon, and Flipkart.

## 🌟 Features

- **Multi-Platform Support**: Analyze content from Twitter, Instagram, YouTube, Amazon, and Flipkart
- **Sentiment Analysis**: Advanced BERT-based sentiment classification (Positive/Negative)
- **Purchase Intent Detection**: Identifies potential buying signals in comments
- **Interactive Dashboard**: Real-time visualization with pie charts and bar graphs
- **User Authentication**: Secure user registration, login, and logout system
- **RESTful API**: Clean API endpoints for data fetching and analysis

## 🛠️ Tech Stack

### Backend
- **Django**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL/SQLite**: Database
- **Transformers (Hugging Face)**: BERT model for sentiment analysis
- **spaCy**: Natural language processing
- **PyTorch**: Deep learning framework

### Frontend
- **React.js**: User interface
- **Material-UI**: UI components
- **Recharts**: Data visualization
- **Axios**: HTTP client

### APIs & Libraries
- **Tweepy**: Twitter API integration
- **Instaloader**: Instagram data extraction
- **YouTube Data API v3**: YouTube comments fetching
- **BeautifulSoup**: Web scraping for e-commerce reviews

## 📁 Project Structure

```
social-media-analysis/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
├── SentimentAI/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── auth.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── social_media_analysis/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```


## 📊 Usage

1. **Access the Dashboard**: Navigate to `http://localhost:3000`
2. **Enter URL**: Paste a URL from supported platforms:
   - Twitter: `https://twitter.com/username/status/tweet_id`
   - Instagram: `https://instagram.com/p/post_id/`
   - YouTube: `https://youtube.com/watch?v=video_id`
   - Amazon: Product page URL
   - Flipkart: Product page URL
3. **Analyze**: Click the "Analyze" button to fetch and analyze comments
4. **View Results**: Interactive charts showing sentiment distribution and purchase intent

## 🔗 API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout

### Analysis
- `GET /api/fetch_comments/` - Test endpoint
- `POST /api/fetch_comments/` - Analyze comments from URL

### Example Request
```bash
curl -X POST http://localhost:8000/api/fetch_comments/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=example"}'
```

### Example Response
```json
{
  "positive_percent": 75.5,
  "negative_percent": 24.5,
  "purchase_intent_percent": 12.3
}
```

## 🗄️ Database Models

### Comment Model
- Platform, content, sentiment, purchase intent
- Categories, entities, topics, keywords
- Summary, trend score, user association

### UserProfile Model
- User preferences and activity tracking
- JSON field for flexible preference storage

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

### Individual Container Build
```bash
# Backend
docker build -t sentiment-backend .

# Frontend
cd frontend
docker build -t sentiment-frontend .
```

## 🔒 Security Considerations

- **API Rate Limits**: Implement rate limiting for API calls
- **Authentication**: JWT tokens recommended for production
- **Environment Variables**: Never commit API keys to version control
- **Input Validation**: Sanitize all user inputs
- **CORS**: Configure proper CORS settings for production

## 🚧 Known Limitations

- Instagram scraping may be rate-limited
- E-commerce scraping depends on website structure changes
- BERT model requires significant computational resources
- Some platforms may block automated requests

## 🔮 Future Enhancements

- [ ] Real-time sentiment tracking
- [ ] Multi-language support
- [ ] Advanced emotion detection
- [ ] Trend analysis over time
- [ ] Export functionality (PDF/CSV)
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Social media posting scheduler



## ⚠️ Disclaimer

This tool is for educational and research purposes. Ensure compliance with platform terms of service and data privacy regulations when scraping data from social media platforms.

---

**Built with ❤️ using Django, React, and AI/ML technologies**
