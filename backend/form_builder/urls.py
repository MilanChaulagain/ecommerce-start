"""
URL patterns for form builder API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormTemplateViewSet, FormSubmissionViewSet, FormFieldTypeViewSet

app_name = 'form_builder'

router = DefaultRouter()
router.register(r'forms', FormTemplateViewSet, basename='form')
router.register(r'submissions', FormSubmissionViewSet, basename='submission')
router.register(r'field-types', FormFieldTypeViewSet, basename='field-type')

urlpatterns = [
    path('', include(router.urls)),
]
