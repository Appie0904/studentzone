from django import forms
from .models import Project, StudyPartner


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'project_type', 'status', 
            'team_size_min', 'team_size_max', 'start_date', 'end_date', 
            'deadline', 'contact_email', 'external_link', 'meeting_schedule'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project...'
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'team_size_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20
            }),
            'team_size_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@example.com'
            }),
            'external_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/...'
            }),
            'meeting_schedule': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Meeting schedule and communication preferences...'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        team_size_min = cleaned_data.get('team_size_min')
        team_size_max = cleaned_data.get('team_size_max')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(
                "End date must be after start date."
            )
        
        if team_size_min and team_size_max and team_size_min > team_size_max:
            raise forms.ValidationError(
                "Minimum team size cannot be greater than maximum team size."
            )
        
        return cleaned_data


class StudyPartnerForm(forms.ModelForm):
    """Form for creating and editing study partner profiles."""
    
    class Meta:
        model = StudyPartner
        fields = [
            'study_field', 'university', 'preferred_study_methods', 
            'subjects_of_interest', 'availability', 'preferred_universities',
            'max_distance_km', 'online_only'
        ]
        widgets = {
            'study_field': forms.Select(attrs={
                'class': 'form-select'
            }),
            'university': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preferred_study_methods': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., group study, online, library'
            }),
            'subjects_of_interest': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Specific subjects or topics you want to study'
            }),
            'availability': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'When you\'re available to study'
            }),
            'preferred_universities': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'max_distance_km': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 500
            }),
            'online_only': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        } 