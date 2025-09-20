from django.urls import path
from .views import fetch_comments, get_analysis_history
from .auth import register_user, login_user, logout_user, check_auth_status

urlpatterns = [
    path('fetch_comments/', fetch_comments, name='fetch_comments'),
    path('history/', get_analysis_history, name='get_analysis_history'),
    
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('auth-status/', check_auth_status, name='check_auth_status'),
]
