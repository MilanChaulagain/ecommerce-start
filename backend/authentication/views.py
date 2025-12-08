"""
Django views for OAuth 2.0 social authentication
"""
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.db import transaction

from .oauth_utils import (
    OAuthHandler, 
    JWTHandler, 
    generate_state_token, 
    normalize_user_data
)
from .models import SocialAccount, UserSession
from .oauth_config import FRONTEND_URL

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class OAuthAuthorizeView(View):
    """
    Step 1: Generate and return OAuth authorization URL
    
    GET /api/auth/<provider>/authorize/
    """
    
    def get(self, request, provider):
        try:
            # Initialize OAuth handler for the provider
            oauth_handler = OAuthHandler(provider)
            
            # Generate state token for CSRF protection
            state = generate_state_token()
            
            # Store state in session
            request.session[f'{provider}_oauth_state'] = state
            
            # Generate authorization URL
            authorization_url = oauth_handler.get_authorization_url(state)
            
            return JsonResponse({
                'authorization_url': authorization_url,
                'provider': provider
            })
        
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to initialize OAuth'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OAuthCallbackView(View):
    """
    Step 2: Handle OAuth callback from provider
    
    GET /api/auth/<provider>/callback/?code=xxx&state=xxx
    """
    
    def get(self, request, provider):
        try:
            # Get authorization code and state from query parameters
            code = request.GET.get('code')
            state = request.GET.get('state')
            error = request.GET.get('error')
            
            # Handle OAuth errors
            if error:
                error_description = request.GET.get('error_description', 'Authorization failed')
                return HttpResponseRedirect(
                    f"{FRONTEND_URL}/auth/callback?error={error}&message={error_description}"
                )
            
            # Validate required parameters
            if not code or not state:
                return HttpResponseRedirect(
                    f"{FRONTEND_URL}/auth/callback?error=invalid_request&message=Missing code or state"
                )
            
            # Verify state token (CSRF protection)
            session_state = request.session.get(f'{provider}_oauth_state')
            if not session_state or session_state != state:
                return HttpResponseRedirect(
                    f"{FRONTEND_URL}/auth/callback?error=invalid_state&message=CSRF verification failed"
                )
            
            # Initialize OAuth handler
            oauth_handler = OAuthHandler(provider)
            
            # Exchange code for access token
            token_data = oauth_handler.exchange_code_for_token(code)
            access_token = token_data.get('access_token')
            
            if not access_token:
                return HttpResponseRedirect(
                    f"{FRONTEND_URL}/auth/callback?error=token_error&message=Failed to get access token"
                )
            
            # Fetch user information from provider
            user_data = oauth_handler.get_user_info(access_token)
            
            # Normalize user data
            normalized_data = normalize_user_data(provider, user_data)
            
            # Create or update user
            user = self._create_or_update_user(
                provider=provider,
                normalized_data=normalized_data,
                access_token=access_token,
                token_data=token_data
            )
            
            # Generate JWT token
            jwt_token, expiration = JWTHandler.generate_token(user.id, user.email)
            
            # Create user session
            session = UserSession.objects.create(
                user=user,
                session_key=generate_state_token(),
                jwt_token=jwt_token,
                expires_at=expiration,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Store JWT in session
            request.session['jwt_token'] = jwt_token
            request.session['user_id'] = user.id
            
            # Clean up OAuth state
            del request.session[f'{provider}_oauth_state']
            
            # Redirect to frontend with success
            return HttpResponseRedirect(
                f"{FRONTEND_URL}/auth/callback?success=true&token={jwt_token}"
            )
        
        except Exception as e:
            print(f"OAuth callback error: {str(e)}")
            return HttpResponseRedirect(
                f"{FRONTEND_URL}/auth/callback?error=server_error&message=Authentication failed"
            )
    
    @transaction.atomic
    def _create_or_update_user(self, provider, normalized_data, access_token, token_data):
        """Create or update user and social account"""
        provider_user_id = normalized_data['provider_user_id']
        
        # Try to find existing social account
        try:
            social_account = SocialAccount.objects.select_related('user').get(
                provider=provider,
                provider_user_id=provider_user_id
            )
            user = social_account.user
            
            # Update user information
            if normalized_data.get('first_name'):
                user.first_name = normalized_data['first_name']
            if normalized_data.get('last_name'):
                user.last_name = normalized_data['last_name']
            if normalized_data.get('profile_picture'):
                user.profile_picture = normalized_data['profile_picture']
            user.save()
            
            # Update social account tokens
            social_account.access_token = access_token
            social_account.refresh_token = token_data.get('refresh_token')
            social_account.extra_data = token_data
            social_account.save()
            
        except SocialAccount.DoesNotExist:
            # Create new user
            email = normalized_data.get('email')
            
            # Generate email if not provided (Instagram case)
            if not email:
                email = f"{provider}_{provider_user_id}@example.com"
            
            # Check if user with this email already exists
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': normalized_data.get('first_name', ''),
                    'last_name': normalized_data.get('last_name', ''),
                    'username': normalized_data.get('username', ''),
                    'profile_picture': normalized_data.get('profile_picture', ''),
                }
            )
            
            # Create social account
            social_account = SocialAccount.objects.create(
                user=user,
                provider=provider,
                provider_user_id=provider_user_id,
                access_token=access_token,
                refresh_token=token_data.get('refresh_token'),
                extra_data=token_data
            )
        
        return user
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@method_decorator(csrf_exempt, name='dispatch')
class CurrentUserView(View):
    """
    Get current authenticated user
    
    GET /api/auth/user/
    """
    
    def get(self, request):
        # Get JWT from session or Authorization header
        jwt_token = request.session.get('jwt_token')
        
        if not jwt_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                jwt_token = auth_header[7:]
        
        if not jwt_token:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        # Decode JWT
        payload = JWTHandler.decode_token(jwt_token)
        
        if not payload:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        
        # Get user
        try:
            user = User.objects.get(id=payload['user_id'])
            
            # Get social accounts
            social_accounts = list(user.social_accounts.values('provider', 'provider_user_id'))
            
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'profile_picture': user.profile_picture,
                'social_accounts': social_accounts,
            })
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    """
    Logout user
    
    POST /api/auth/logout/
    """
    
    def post(self, request):
        jwt_token = request.session.get('jwt_token')
        
        if jwt_token:
            # Deactivate session
            UserSession.objects.filter(jwt_token=jwt_token).update(is_active=False)
        
        # Clear session
        request.session.flush()
        
        return JsonResponse({'message': 'Logged out successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(View):
    """
    Refresh JWT token
    
    POST /api/auth/refresh/
    """
    
    def post(self, request):
        jwt_token = request.session.get('jwt_token')
        
        if not jwt_token:
            return JsonResponse({'error': 'No token provided'}, status=401)
        
        # Refresh token
        result = JWTHandler.refresh_token(jwt_token)
        
        if not result:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        
        new_token, expiration = result
        
        # Update session
        request.session['jwt_token'] = new_token
        
        # Update user session
        UserSession.objects.filter(jwt_token=jwt_token).update(
            jwt_token=new_token,
            expires_at=expiration
        )
        
        return JsonResponse({
            'token': new_token,
            'expires_at': expiration.isoformat()
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(View):
    """
    Admin login endpoint with email/password authentication
    
    POST /api/auth/admin/login/
    Body: { "email": "admin@example.com", "password": "password" }
    """
    
    def post(self, request):
        try:
            from django.utils import timezone
            
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({
                    'error': 'Email and password are required'
                }, status=400)
            
            # Get user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    'error': 'Invalid credentials'
                }, status=401)
            
            # Check password
            if not user.check_password(password):
                return JsonResponse({
                    'error': 'Invalid credentials'
                }, status=401)
            
            # Check if user is admin
            if not user.is_staff and not user.is_superuser:
                return JsonResponse({
                    'error': 'Access denied. Admin privileges required.'
                }, status=403)
            
            # Check if user is active
            if not user.is_active:
                return JsonResponse({
                    'error': 'Account is inactive'
                }, status=403)
            
            # Generate JWT token
            token, expiration = JWTHandler.generate_token(user.id, user.email)
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Create session record with unique session key
            session = UserSession.objects.create(
                user=user,
                session_key=generate_state_token(),  # Generate unique session key
                jwt_token=token,
                expires_at=expiration,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return JsonResponse({
                'token': token,
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'name': user.get_full_name(),
                    'user_type': user.user_type,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'permissions': {
                        'can_build_forms': user.can_build_forms,
                        'can_manage_users': user.can_manage_users,
                        'can_view_analytics': user.can_view_analytics,
                    }
                }
            })
        
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
