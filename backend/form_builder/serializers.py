"""
Serializers for form builder API
"""
from rest_framework import serializers
from .models import FormTemplate, FormSubmission, FormFieldType
from django.contrib.auth import get_user_model

User = get_user_model()


class FormFieldTypeSerializer(serializers.ModelSerializer):
    """Serializer for form field types"""
    class Meta:
        model = FormFieldType
        fields = ['id', 'name', 'label', 'icon', 'validation_rules', 'is_active']


class FormTemplateSerializer(serializers.ModelSerializer):
    """Serializer for form templates"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True, allow_null=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = FormTemplate
        fields = [
            'id', 'name', 'description', 'slug', 'schema', 
            'is_active', 'allow_anonymous', 'submission_count',
            'created_by', 'created_by_email', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'submission_count', 'created_at', 'updated_at', 'created_by', 'created_by_email', 'created_by_name']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class FormTemplateListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for form list view"""
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = FormTemplate
        fields = [
            'id', 'name', 'description', 'slug', 
            'is_active', 'submission_count',
            'created_by_name', 'created_at', 'updated_at'
        ]
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class FormSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for form submissions"""
    form_name = serializers.CharField(source='form_template.name', read_only=True)
    submitted_by_email = serializers.EmailField(source='submitted_by.email', read_only=True)
    
    class Meta:
        model = FormSubmission
        fields = [
            'id', 'form_template', 'form_name', 'data', 
            'submitted_by', 'submitted_by_email',
            'ip_address', 'user_agent', 'submitted_at',
            'status', 'notes'
        ]
        read_only_fields = ['id', 'submitted_at']
