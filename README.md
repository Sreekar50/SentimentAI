# Social Media Sentiment Analysis
## (Django Rest Framework, React, MySQL)
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

