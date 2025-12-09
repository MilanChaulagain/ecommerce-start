// Type definitions for Form Builder
import { LucideIcon } from 'lucide-react';

export type FieldType = 'text' | 'email' | 'number' | 'tel' | 'textarea' | 'date' | 'time' | 'select' | 'checkbox' | 'radio' | 'url';

export interface FieldOption {
  value: string;
  label: string;
}

export interface FormField {
  id: string;
  type: FieldType;
  label: string;
  name: string;
  placeholder?: string;
  required: boolean;
  options?: FieldOption[];
  defaultValue?: string;
  defaultChecked?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  allowMultiple?: boolean;
}

export interface FieldTypeDefinition {
  type: FieldType;
  label: string;
  icon: LucideIcon;
}

export interface FormTemplate {
  id?: string;
  name: string;
  description?: string;
  schema: {
    fields: FormField[];
  };
}

export interface FormBuilderState {
  formId: string | null;
  formName: string;
  formDescription: string;
  fields: FormField[];
  selectedField: FormField | null;
  isEditMode: boolean;
  showPreview: boolean;
}
