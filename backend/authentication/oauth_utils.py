"""
Utility functions for OAuth 2.0 authentication and JWT handling
"""
import jwt
import secrets
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
from typing import Dict, Optional, Tuple

from .oauth_config import OAuthConfig, JWT_CONFIG


class OAuthHandler:
    """Handle OAuth 2.0 authentication flow"""
    
    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.config = OAuthConfig.get_config(self.provider)
        
        if not self.config:
            raise ValueError(f"Unknown OAuth provider: {provider}")
    
    def get_authorization_url(self, state: str) -> str:
        """
        Generate OAuth authorization URL
        
        Step 1 of OAuth 2.0: Redirect user to provider's authorization page
        """
        params = {
            'response_type': 'code',
            'state': state,
        }
        
        if self.provider == 'facebook':
            params.update({
                'client_id': self.config['client_id'],
                'redirect_uri': self.config['redirect_uri'],
                'scope': ','.join(self.config['scope']),
            })
        
        elif self.provider == 'instagram':
            params.update({
                'client_id': self.config['client_id'],
                'redirect_uri': self.config['redirect_uri'],
                'scope': ','.join(self.config['scope']),
            })
        
        elif self.provider == 'tiktok':
            params.update({
                'client_key': self.config['client_key'],
                'redirect_uri': self.config['redirect_uri'],
                'scope': ','.join(self.config['scope']),
            })
        
        return f"{self.config['authorization_url']}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Step 2 of OAuth 2.0: Exchange code received from provider for access token
        """
        if self.provider == 'facebook':
            return self._exchange_facebook_token(code)
        elif self.provider == 'instagram':
            return self._exchange_instagram_token(code)
        elif self.provider == 'tiktok':
            return self._exchange_tiktok_token(code)
    
    def _exchange_facebook_token(self, code: str) -> Dict:
        """Exchange Facebook authorization code for access token"""
        params = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'code': code,
            'redirect_uri': self.config['redirect_uri'],
        }
        
        response = requests.get(self.config['token_url'], params=params)
        response.raise_for_status()
        return response.json()
    
    def _exchange_instagram_token(self, code: str) -> Dict:
        """Exchange Instagram authorization code for access token"""
        data = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config['redirect_uri'],
        }
        
        response = requests.post(self.config['token_url'], data=data)
        response.raise_for_status()
        return response.json()
    
    def _exchange_tiktok_token(self, code: str) -> Dict:
        """Exchange TikTok authorization code for access token"""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        data = {
            'client_key': self.config['client_key'],
            'client_secret': self.config['client_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config['redirect_uri'],
        }
        
        response = requests.post(self.config['token_url'], headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, access_token: str) -> Dict:
        """
        Fetch user profile information from OAuth provider
        
        Step 3 of OAuth 2.0: Use access token to retrieve user data
        """
        if self.provider == 'facebook':
            return self._get_facebook_user_info(access_token)
        elif self.provider == 'instagram':
            return self._get_instagram_user_info(access_token)
        elif self.provider == 'tiktok':
            return self._get_tiktok_user_info(access_token)
    
    def _get_facebook_user_info(self, access_token: str) -> Dict:
        """Fetch Facebook user profile"""
        params = {
            'fields': self.config['user_fields'],
            'access_token': access_token,
        }
        
        response = requests.get(self.config['user_info_url'], params=params)
        response.raise_for_status()
        return response.json()
    
    def _get_instagram_user_info(self, access_token: str) -> Dict:
        """Fetch Instagram user profile"""
        params = {
            'fields': self.config['user_fields'],
            'access_token': access_token,
        }
        
        response = requests.get(self.config['user_info_url'], params=params)
        response.raise_for_status()
        return response.json()
    
    def _get_tiktok_user_info(self, access_token: str) -> Dict:
        """Fetch TikTok user profile"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        response = requests.get(self.config['user_info_url'], headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # TikTok returns data in a nested structure
        if 'data' in data and 'user' in data['data']:
            return data['data']['user']
        return data


class JWTHandler:
    """Handle JWT token generation and validation"""
    
    @staticmethod
    def generate_token(user_id: int, email: str) -> Tuple[str, datetime]:
        """Generate JWT token for authenticated user"""
        expiration = datetime.utcnow() + timedelta(hours=JWT_CONFIG['expiration_hours'])
        
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': expiration,
            'iat': datetime.utcnow(),
        }
        
        token = jwt.encode(
            payload,
            JWT_CONFIG['secret_key'],
            algorithm=JWT_CONFIG['algorithm']
        )
        
        return token, expiration
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                JWT_CONFIG['secret_key'],
                algorithms=[JWT_CONFIG['algorithm']]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def refresh_token(token: str) -> Optional[Tuple[str, datetime]]:
        """Refresh an existing JWT token"""
        payload = JWTHandler.decode_token(token)
        
        if not payload:
            return None
        
        return JWTHandler.generate_token(
            payload['user_id'],
            payload['email']
        )


def generate_state_token() -> str:
    """Generate a random state token for CSRF protection"""
    return secrets.token_urlsafe(32)


def normalize_user_data(provider: str, user_data: Dict) -> Dict:
    """
    Normalize user data from different OAuth providers to a common format
    """
    normalized = {
        'provider_user_id': None,
        'email': None,
        'first_name': '',
        'last_name': '',
        'username': '',
        'profile_picture': '',
    }
    
    if provider == 'facebook':
        normalized['provider_user_id'] = user_data.get('id')
        normalized['email'] = user_data.get('email')
        normalized['first_name'] = user_data.get('first_name', '')
        normalized['last_name'] = user_data.get('last_name', '')
        
        if 'picture' in user_data and 'data' in user_data['picture']:
            normalized['profile_picture'] = user_data['picture']['data'].get('url', '')
    
    elif provider == 'instagram':
        normalized['provider_user_id'] = user_data.get('id')
        normalized['username'] = user_data.get('username', '')
        # Instagram Basic Display API doesn't provide email
        # You'll need to handle this case appropriately
    
    elif provider == 'tiktok':
        normalized['provider_user_id'] = user_data.get('open_id')
        normalized['username'] = user_data.get('display_name', '')
        normalized['profile_picture'] = user_data.get('avatar_url', '')
    
    return normalized
