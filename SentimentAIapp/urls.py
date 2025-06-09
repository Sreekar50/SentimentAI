from django.urls import path
from .views import fetch_comments
from .auth import register_user, login_user, logout_user

urlpatterns = [
    path('fetch_comments/', fetch_comments, name='fetch_comments'),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
]

