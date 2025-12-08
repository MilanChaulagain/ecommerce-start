# Django OAuth 2.0 Social Authentication Backend

This Django backend provides OAuth 2.0 authentication for Facebook, Instagram, and TikTok.

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Django Project
```bash
django-admin startproject ecommerce_backend .
python manage.py startapp authentication
```

### 3. Configure OAuth Apps

#### Facebook OAuth
1. Go to https://developers.facebook.com/
2. Create a new app
3. Get your App ID and App Secret
4. Add redirect URI: `http://localhost:8000/api/auth/facebook/callback/`

#### Instagram OAuth
1. Go to https://developers.facebook.com/ (Instagram uses Facebook's platform)
2. Add Instagram Basic Display product to your app
3. Get Client ID and Client Secret
4. Add redirect URI: `http://localhost:8000/api/auth/instagram/callback/`

#### TikTok OAuth
1. Go to https://developers.tiktok.com/
2. Create a new app
3. Get Client Key and Client Secret
4. Add redirect URI: `http://localhost:8000/api/auth/tiktok/callback/`

### 4. Environment Variables

Create `.env` file in backend directory:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Database
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Facebook OAuth
FACEBOOK_CLIENT_ID=your_facebook_app_id
FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/auth/facebook/callback/

# Instagram OAuth
INSTAGRAM_CLIENT_ID=your_instagram_client_id
INSTAGRAM_CLIENT_SECRET=your_instagram_client_secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/auth/instagram/callback/

# TikTok OAuth
TIKTOK_CLIENT_KEY=your_tiktok_client_key
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret
TIKTOK_REDIRECT_URI=http://localhost:8000/api/auth/tiktok/callback/

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## OAuth 2.0 Flow

1. **Authorization Request**: User clicks social login button
2. **Redirect to Provider**: Backend generates authorization URL
3. **User Consent**: User grants permissions on provider's site
4. **Callback with Code**: Provider redirects back with authorization code
5. **Token Exchange**: Backend exchanges code for access token
6. **Fetch User Profile**: Backend retrieves user data from provider
7. **Create/Update User**: User is created or updated in database
8. **Generate JWT**: Backend generates JWT token for authentication
9. **Return to Frontend**: User is authenticated and redirected

## API Endpoints

- `GET /api/auth/<provider>/authorize/` - Get OAuth authorization URL
- `GET /api/auth/<provider>/callback/` - OAuth callback handler
- `GET /api/auth/user/` - Get current authenticated user
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/refresh/` - Refresh JWT token

## Frontend Integration

Set environment variable in Next.js:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
