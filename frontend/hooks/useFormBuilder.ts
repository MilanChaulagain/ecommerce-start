'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { FormField, FieldType, FormBuilderState } from '@/lib/form-builder-types';

export function useFormBuilder() {
  const searchParams = useSearchParams();
  const formIdFromUrl = searchParams.get('id');

  const [state, setState] = useState<FormBuilderState>({
    formId: null,
    formName: '',
    formDescription: '',
    fields: [],
    selectedField: null,
    isEditMode: false,
    showPreview: false,
  });

  const [loading, setLoading] = useState(false);

  // Load form data if editing
  useEffect(() => {
    if (formIdFromUrl) {
      loadForm(formIdFromUrl);
    }
  }, [formIdFromUrl]);

  const loadForm = async (id: string) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await fetch(`http://localhost:8000/api/forms/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setState(prev => ({
          ...prev,
          formId: data.id,
          formName: data.name,
          formDescription: data.description || '',
          fields: data.schema?.fields || [],
          isEditMode: true,
        }));
      } else {
        alert('Failed to load form');
      }
    } catch (error) {
      console.error('Error loading form:', error);
      alert('Failed to load form');
    } finally {
      setLoading(false);
    }
  };

  const addField = (type: FieldType) => {
    const newField: FormField = {
      id: `field_${Date.now()}`,
      type,
      label: `${type.charAt(0).toUpperCase() + type.slice(1)} Field`,
      name: `field_${state.fields.length + 1}`,
      placeholder: type === 'select' ? 'Select an option' : `Enter ${type}`,
      required: false,
      options: (type === 'select' || type === 'radio') ? [
        { value: 'option_1', label: 'Option 1' },
        { value: 'option_2', label: 'Option 2' },
        { value: 'option_3', label: 'Option 3' },
      ] : undefined,
    };

    setState(prev => ({
      ...prev,
      fields: [...prev.fields, newField],
      selectedField: newField,
    }));
  };

  const updateField = (updates: Partial<FormField>) => {
    if (!state.selectedField) return;

    setState(prev => ({
      ...prev,
      fields: prev.fields.map(f => 
        f.id === state.selectedField?.id ? { ...f, ...updates } : f
      ),
      selectedField: state.selectedField ? { ...state.selectedField, ...updates } : null,
    }));
  };

  const deleteField = (fieldId: string) => {
    setState(prev => ({
      ...prev,
      fields: prev.fields.filter(f => f.id !== fieldId),
      selectedField: prev.selectedField?.id === fieldId ? null : prev.selectedField,
    }));
  };

  const selectField = (field: FormField) => {
    setState(prev => ({ ...prev, selectedField: field }));
  };

  const reorderFields = (newFields: FormField[]) => {
    setState(prev => ({ ...prev, fields: newFields }));
  };

  const saveForm = async () => {
    if (!state.formName.trim()) {
      alert('Please enter a form name');
      return;
    }

    if (state.fields.length === 0) {
      alert('Please add at least one field');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('admin_token');
      const payload = {
        name: state.formName,
        description: state.formDescription,
        schema: {
          fields: state.fields,
        },
      };

      const url = state.isEditMode
        ? `http://localhost:8000/api/forms/${state.formId}/`
        : 'http://localhost:8000/api/forms/';

      const method = state.isEditMode ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Form ${state.isEditMode ? 'updated' : 'created'} successfully!`);
        
        if (!state.isEditMode) {
          // Clear form after creation
          setState({
            formId: null,
            formName: '',
            formDescription: '',
            fields: [],
            selectedField: null,
            isEditMode: false,
            showPreview: false,
          });
        } else {
          // Keep form data after update
          setState(prev => ({ ...prev, formId: data.id }));
        }
      } else {
        const errorData = await response.json();
        alert(`Failed to save form: ${JSON.stringify(errorData)}`);
      }
    } catch (error) {
      console.error('Error saving form:', error);
      alert('Failed to save form');
    } finally {
      setLoading(false);
    }
  };

  const togglePreview = () => {
    setState(prev => ({ ...prev, showPreview: !prev.showPreview }));
  };

  const updateFormMetadata = (updates: { formName?: string; formDescription?: string }) => {
    setState(prev => ({
      ...prev,
      formName: updates.formName ?? prev.formName,
      formDescription: updates.formDescription ?? prev.formDescription,
    }));
  };

  return {
    state,
    loading,
    addField,
    updateField,
    deleteField,
    selectField,
    reorderFields,
    saveForm,
    togglePreview,
    updateFormMetadata,
  };
}
