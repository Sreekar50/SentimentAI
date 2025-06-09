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

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-analysis
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install django djangorestframework transformers torch spacy tweepy instaloader google-api-python-client beautifulsoup4 requests pandas
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Configure API credentials in `views.py`:
```python
# Twitter API credentials
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

# YouTube API Key
YOUTUBE_API_KEY = "your_youtube_api_key"

# Instagram credentials (in fetch_instagram_comments function)
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
```

6. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Start the Django server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

## 🔧 API Configuration

### Required API Keys

1. **Twitter API**: Get credentials from [Twitter Developer Portal](https://developer.twitter.com/)
2. **YouTube API**: Obtain key from [Google Cloud Console](https://console.cloud.google.com/)
3. **Instagram**: Use your Instagram credentials (consider using Instagram Basic Display API for production)

### Environment Variables

Create a `.env` file in the root directory:
```env
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
YOUTUBE_API_KEY=your_youtube_api_key
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@example.com or create an issue in the GitHub repository.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Ensure compliance with platform terms of service and data privacy regulations when scraping data from social media platforms.

---

**Built with ❤️ using Django, React, and AI/ML technologies**
