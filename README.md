# Social Media Sentiment Analysis

A full-stack web application that analyzes sentiment and purchase intent from social media comments and e-commerce reviews. Built with Django REST Framework backend and React frontend.

## 🚀 Features

- **Multi-Platform Support**: Analyze comments from Twitter, Instagram, YouTube, Amazon, and Flipkart
- **Sentiment Analysis**: Advanced sentiment classification using BERT models
- **Purchase Intent Detection**: Identify potential buying signals in comments
- **User Authentication**: Secure token-based authentication system
- **Data Visualization**: Interactive charts and graphs using Recharts
- **Analysis History**: Track and view previous analysis results
- **Real-time Processing**: Process and analyze comments in real-time

## 🛠️ Tech Stack

### Backend
- **Django 5.1.7** - Web framework
- **Django REST Framework** - API development
- **MySQL** - Database
- **Transformers** - BERT models for sentiment analysis
- **Tweepy** - Twitter API integration
- **Instaloader** - Instagram data extraction
- **YouTube Data API** - YouTube comments
- **BeautifulSoup** - Web scraping for e-commerce sites

### Frontend
- **React 18** - User interface
- **Material-UI** - UI components
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Styling

### AI/ML
- **BERT (nlptown/bert-base-multilingual-uncased-sentiment)** - Sentiment analysis
- **spaCy** - Natural language processing
- **PyTorch** - Deep learning framework

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-media-sentiment-analysis.git
cd social-media-sentiment-analysis
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install additional ML models
python -m spacy download en_core_web_sm
```

### 3. Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE socialdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Run migrations
python manage.py makemigrations
python manage.py makemigrations SentimentAI
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Configure API Keys

Create a `.env` file in the root directory and add your API keys:

```env
# Twitter API Keys
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret

# YouTube API Key
YOUTUBE_API_KEY=your_youtube_api_key

# Instagram Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Database Configuration
DB_NAME=socialdb
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

## 🚀 Running the Application

### Start the Backend Server

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Django server
python manage.py runserver
```

The backend API will be available at: `http://127.0.0.1:8000`

### Start the Frontend Server

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start React development server
npm start
```

The frontend will be available at: `http://localhost:3000`

## 📱 Usage

1. **Registration**: Create a new account with username and password
2. **Login**: Sign in with your credentials to access the dashboard
3. **URL Analysis**: Enter a social media or e-commerce URL in the input field
4. **View Results**: See sentiment distribution and purchase intent analysis
5. **History**: Review previous analysis results in your account

### Supported URL Formats

- **Twitter**: `https://twitter.com/username/status/tweet_id`
- **Instagram**: `https://instagram.com/p/post_id/` or `https://instagram.com/reel/reel_id/`
- **YouTube**: `https://youtube.com/watch?v=video_id` or `https://youtu.be/video_id`
- **Amazon**: `https://amazon.com/product-name/dp/product_id`
- **Flipkart**: `https://flipkart.com/product-name/p/product_id`

## 🔗 API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `GET /api/auth-status/` - Check authentication status

### Analysis
- `POST /api/fetch_comments/` - Analyze URL for sentiment and purchase intent
- `GET /api/history/` - Get user's analysis history

## 📊 Database Schema

### Models

**User** (Django's built-in User model)
- username, email, password, etc.

**UserProfile**
- user (OneToOne with User)
- preferences (JSON)
- last_activity (DateTime)
- is_premium (Boolean)

**Comment**
- platform (CharField)
- content (TextField)
- sentiment (CharField)
- purchase_intent (Boolean)
- user (ForeignKey to User)
- created_at (DateTime)

**AnalysisHistory**
- user (ForeignKey to User)
- url (URLField)
- platform (CharField)
- positive_percent (Float)
- negative_percent (Float)
- purchase_intent_percent (Float)
- total_comments (Integer)
- created_at (DateTime)

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Features

- Token-based authentication
- CORS protection
- CSRF protection
- Input validation
- SQL injection prevention
- XSS protection

## 📈 Performance Considerations

- Database indexing on frequently queried fields
- Pagination for large datasets
- Caching for repeated API calls
- Optimized database queries
- Efficient sentiment analysis processing


## 🙏 Acknowledgments

- **Hugging Face Transformers** for BERT models
- **Material-UI** for beautiful React components
- **Recharts** for data visualization
- **Django REST Framework** for robust API development

## 🐛 Known Issues

- Instagram scraping may be rate-limited
- Some social media platforms may require additional authentication
- Large datasets may take longer to process


## 🔮 Future Enhancements

- [ ] Real-time sentiment monitoring
- [ ] Advanced analytics dashboard
- [ ] Export analysis results
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] API rate limiting
- [ ] Advanced filtering options
- [ ] Scheduled analysis jobs

---

**Made with ❤️ by Your Team**
