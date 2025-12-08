"""
Form Builder Admin Interface
"""
from django.contrib import admin
from .models import FormTemplate, FormSubmission, FormFieldType


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_by', 'is_active', 'submission_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'slug']
    readonly_fields = ['id', 'created_at', 'updated_at', 'submission_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'created_by')
        }),
        ('Form Schema', {
            'fields': ('schema',),
            'classes': ('wide',)
        }),
        ('Settings', {
            'fields': ('is_active', 'allow_anonymous', 'enable_email_notifications', 'notification_email')
        }),
        ('Metadata', {
            'fields': ('id', 'submission_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['form_template', 'submitted_by', 'status', 'submitted_at', 'ip_address']
    list_filter = ['status', 'submitted_at', 'form_template']
    search_fields = ['data', 'notes']
    readonly_fields = ['id', 'submitted_at', 'ip_address', 'user_agent']
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('form_template', 'submitted_by', 'status')
        }),
        ('Data', {
            'fields': ('data',),
            'classes': ('wide',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('id', 'ip_address', 'user_agent', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormFieldType)
class FormFieldTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'field_type', 'icon', 'is_active', 'display_order']
    list_filter = ['field_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['display_order', 'name']
