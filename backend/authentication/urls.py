"""
URL patterns for authentication endpoints
"""
from django.urls import path
from .views import (
    OAuthAuthorizeView,
    OAuthCallbackView,
    CurrentUserView,
    LogoutView,
    RefreshTokenView,
    AdminLoginView,
)

app_name = 'authentication'

urlpatterns = [
    # Admin login
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    
    # OAuth Authorization - Step 1: Get authorization URL
    path('<str:provider>/authorize/', OAuthAuthorizeView.as_view(), name='oauth_authorize'),
    
    # OAuth Callback - Step 2: Handle provider redirect
    path('<str:provider>/callback/', OAuthCallbackView.as_view(), name='oauth_callback'),
    
    # User management
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh_token'),
]
