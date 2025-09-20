from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import json
import secrets
import hashlib

user_tokens = {}

def generate_token():
    """Generate a secure token"""
    return secrets.token_urlsafe(32)

def hash_token(token):
    """Hash token for storage"""
    return hashlib.sha256(token.encode()).hexdigest()

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.data.get('username')
            password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(username.strip()) < 3:
            return Response({'error': 'Username must be at least 3 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        try:
            UserProfile.objects.create(user=user)
        except Exception as profile_error:
            print(f"Profile creation error: {profile_error}")
        
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
        
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Registration failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.data.get('username')
            password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                token = generate_token()
                user_tokens[hash_token(token)] = {
                    'user_id': user.id,
                    'username': user.username
                }
                
                try:
                    profile, created = UserProfile.objects.get_or_create(user=user)
                    if not created:
                        profile.save()  
                except Exception as profile_error:
                    print(f"Profile update error: {profile_error}")
                
                return Response({
                    'message': 'Login successful',
                    'username': username,
                    'user_id': user.id,
                    'token': token  
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is disabled'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Login failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def logout_user(request):
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            token_hash = hash_token(token)
            if token_hash in user_tokens:
                del user_tokens[token_hash]
        
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Logout failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def check_auth_status(request):
    """Check if user is authenticated via token"""
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            token_hash = hash_token(token)
            
            if token_hash in user_tokens:
                user_data = user_tokens[token_hash]
                return Response({
                    'authenticated': True,
                    'username': user_data['username'],
                    'user_id': user_data['user_id']
                }, status=status.HTTP_200_OK)
        
        return Response({
            'authenticated': False
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'authenticated': False,
            'error': str(e)
        }, status=status.HTTP_200_OK)

def get_user_from_token(request):
    """Helper function to get user from token"""
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            token_hash = hash_token(token)
            
            if token_hash in user_tokens:
                user_data = user_tokens[token_hash]
                return User.objects.get(id=user_data['user_id'])
        
        return None
    except Exception as e:
        print(f"Token auth error: {e}")
        return None
