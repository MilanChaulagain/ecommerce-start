"""
OAuth 2.0 configuration for social authentication providers
"""
import os
from decouple import config


class OAuthConfig:
    """OAuth 2.0 configuration for different providers"""
    
    # Facebook OAuth Configuration
    FACEBOOK = {
        'client_id': config('FACEBOOK_CLIENT_ID', default=''),
        'client_secret': config('FACEBOOK_CLIENT_SECRET', default=''),
        'redirect_uri': config('FACEBOOK_REDIRECT_URI', default='http://localhost:8000/api/auth/facebook/callback/'),
        'authorization_url': 'https://www.facebook.com/v18.0/dialog/oauth',
        'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
        'user_info_url': 'https://graph.facebook.com/me',
        'scope': ['email', 'public_profile'],
        'user_fields': 'id,email,first_name,last_name,picture',
    }
    
    # Instagram OAuth Configuration
    INSTAGRAM = {
        'client_id': config('INSTAGRAM_CLIENT_ID', default=''),
        'client_secret': config('INSTAGRAM_CLIENT_SECRET', default=''),
        'redirect_uri': config('INSTAGRAM_REDIRECT_URI', default='http://localhost:8000/api/auth/instagram/callback/'),
        'authorization_url': 'https://api.instagram.com/oauth/authorize',
        'token_url': 'https://api.instagram.com/oauth/access_token',
        'user_info_url': 'https://graph.instagram.com/me',
        'scope': ['user_profile', 'user_media'],
        'user_fields': 'id,username,account_type',
    }
    
    # TikTok OAuth Configuration
    TIKTOK = {
        'client_key': config('TIKTOK_CLIENT_KEY', default=''),
        'client_secret': config('TIKTOK_CLIENT_SECRET', default=''),
        'redirect_uri': config('TIKTOK_REDIRECT_URI', default='http://localhost:8000/api/auth/tiktok/callback/'),
        'authorization_url': 'https://www.tiktok.com/v2/auth/authorize/',
        'token_url': 'https://open.tiktokapis.com/v2/oauth/token/',
        'user_info_url': 'https://open.tiktokapis.com/v2/user/info/',
        'scope': ['user.info.basic'],
    }
    
    @classmethod
    def get_config(cls, provider):
        """Get configuration for a specific provider"""
        provider_map = {
            'facebook': cls.FACEBOOK,
            'instagram': cls.INSTAGRAM,
            'tiktok': cls.TIKTOK,
        }
        return provider_map.get(provider.lower())


# JWT Configuration
JWT_CONFIG = {
    'secret_key': config('JWT_SECRET_KEY', default='your-secret-key'),
    'algorithm': config('JWT_ALGORITHM', default='HS256'),
    'expiration_hours': int(config('JWT_EXPIRATION_HOURS', default=24)),
}

# Frontend URL for redirects
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')
