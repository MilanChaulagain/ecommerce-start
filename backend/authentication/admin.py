"""
Django admin configuration for authentication models
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SocialAccount, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """Admin interface for SocialAccount model"""
    
    list_display = ['user', 'provider', 'provider_user_id', 'created_at', 'updated_at']
    list_filter = ['provider', 'created_at']
    search_fields = ['user__email', 'provider_user_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {'fields': ('user', 'provider', 'provider_user_id')}),
        ('Tokens', {'fields': ('access_token', 'refresh_token', 'token_expires_at')}),
        ('Extra Data', {'fields': ('extra_data',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin interface for UserSession model"""
    
    list_display = ['user', 'session_key', 'is_active', 'created_at', 'expires_at', 'last_activity']
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['user__email', 'session_key', 'ip_address']
    readonly_fields = ['created_at', 'last_activity']
    
    fieldsets = (
        (None, {'fields': ('user', 'session_key', 'is_active')}),
        ('Token', {'fields': ('jwt_token',)}),
        ('Session Info', {'fields': ('ip_address', 'user_agent')}),
        ('Timestamps', {'fields': ('created_at', 'expires_at', 'last_activity')}),
    )
