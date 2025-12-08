"""
Form Builder Models
Dynamic form creation and submission handling
"""
import uuid
from django.db import models
from django.conf import settings


class FormTemplate(models.Model):
    """Stores dynamic form templates created by admins"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_forms',
        null=True,
        blank=True
    )
    
    # JSON schema for form structure
    schema = models.JSONField(default=dict)
    # Example schema:
    # {
    #   "fields": [
    #     {
    #       "id": "field_1",
    #       "name": "full_name",
    #       "type": "text",
    #       "label": "Full Name",
    #       "placeholder": "Enter your full name",
    #       "required": true,
    #       "validation": {"minLength": 2, "maxLength": 100}
    #     },
    #     {
    #       "id": "field_2",
    #       "name": "email",
    #       "type": "email",
    #       "label": "Email Address",
    #       "required": true,
    #       "validation": {"pattern": "email"}
    #     }
    #   ],
    #   "settings": {
    #     "submitButtonText": "Submit",
    #     "successMessage": "Form submitted successfully!",
    #     "allowAnonymous": true,
    #     "enableCaptcha": false
    #   }
    # }
    
    # Form settings
    is_active = models.BooleanField(default=True)
    allow_anonymous = models.BooleanField(default=True)
    enable_email_notifications = models.BooleanField(default=False)
    notification_email = models.EmailField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'form_templates'
        ordering = ['-created_at']
        verbose_name = 'Form Template'
        verbose_name_plural = 'Form Templates'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure unique slug
            while FormTemplate.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def increment_submission_count(self):
        """Increment submission counter"""
        self.submission_count += 1
        self.save(update_fields=['submission_count'])


class FormSubmission(models.Model):
    """Stores form submission data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='form_submissions'
    )
    
    # JSON field for dynamic submission data
    data = models.JSONField(default=dict)
    # Example: {"full_name": "John Doe", "email": "john@example.com", "message": "Hello"}
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Status tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'form_submissions'
        ordering = ['-submitted_at']
        verbose_name = 'Form Submission'
        verbose_name_plural = 'Form Submissions'
        indexes = [
            models.Index(fields=['-submitted_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.form_template.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class FormFieldType(models.Model):
    """Predefined field types for form builder palette"""
    
    FIELD_TYPE_CHOICES = [
        ('text', 'Text Input'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('tel', 'Phone Number'),
        ('textarea', 'Text Area'),
        ('select', 'Dropdown'),
        ('radio', 'Radio Button'),
        ('checkbox', 'Checkbox'),
        ('date', 'Date Picker'),
        ('time', 'Time Picker'),
        ('file', 'File Upload'),
        ('url', 'URL'),
        ('range', 'Range Slider'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True)  # Icon name or emoji
    description = models.TextField(blank=True)
    default_validation = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'form_field_types'
        ordering = ['display_order', 'name']
        verbose_name = 'Form Field Type'
        verbose_name_plural = 'Form Field Types'
    
    def __str__(self):
        return self.name
