"""
Views for form builder API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import FormTemplate, FormSubmission, FormFieldType
from .serializers import (
    FormTemplateSerializer, 
    FormTemplateListSerializer,
    FormSubmissionSerializer,
    FormFieldTypeSerializer
)


class FormTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing form templates
    
    list: GET /api/forms/ - Get all forms
    create: POST /api/forms/ - Create new form
    retrieve: GET /api/forms/{id}/ - Get form details
    update: PUT /api/forms/{id}/ - Update form
    partial_update: PATCH /api/forms/{id}/ - Partial update
    destroy: DELETE /api/forms/{id}/ - Delete form
    """
    queryset = FormTemplate.objects.all()
    permission_classes = []  # Open for now, add authentication later
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FormTemplateListSerializer
        return FormTemplateSerializer
    
    def get_queryset(self):
        queryset = FormTemplate.objects.all().order_by('-created_at')
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        # Get user from token if available
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for a form"""
        form = self.get_object()
        submissions = FormSubmission.objects.filter(form_template=form).order_by('-submitted_at')
        serializer = FormSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a form"""
        form = self.get_object()
        form.pk = None
        form.name = f"{form.name} (Copy)"
        form.slug = None  # Will be auto-generated
        form.save()
        serializer = self.get_serializer(form)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FormSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing form submissions
    
    list: GET /api/submissions/ - Get all submissions
    create: POST /api/submissions/ - Submit form
    retrieve: GET /api/submissions/{id}/ - Get submission details
    update: PUT /api/submissions/{id}/ - Update submission
    destroy: DELETE /api/submissions/{id}/ - Delete submission
    """
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    permission_classes = []  # Open for now
    
    def get_queryset(self):
        queryset = FormSubmission.objects.all().order_by('-submitted_at')
        
        # Filter by form template
        form_id = self.request.query_params.get('form_template', None)
        if form_id:
            queryset = queryset.filter(form_template_id=form_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        # Capture IP and user agent
        ip_address = self.request.META.get('REMOTE_ADDR', '')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Get user if authenticated
        user = self.request.user if self.request.user.is_authenticated else None
        
        submission = serializer.save(
            submitted_by=user,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Increment submission count
        submission.form_template.submission_count += 1
        submission.form_template.save(update_fields=['submission_count'])


class FormFieldTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for form field types (read-only)
    
    list: GET /api/field-types/ - Get all field types
    retrieve: GET /api/field-types/{id}/ - Get field type details
    """
    queryset = FormFieldType.objects.filter(is_active=True)
    serializer_class = FormFieldTypeSerializer
    permission_classes = []
