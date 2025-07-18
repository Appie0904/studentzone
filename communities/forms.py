from django import forms
from .models import Community, CommunityEvent


class CommunityForm(forms.ModelForm):
    """Form for creating and editing communities."""
    
    class Meta:
        model = Community
        fields = [
            'name', 'description', 'study_field', 'rules', 
            'is_public'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter community name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your community...'
            }),
            'study_field': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Community rules and guidelines...'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CommunityEventForm(forms.ModelForm):
    """Form for creating and editing community events."""
    
    class Meta:
        model = CommunityEvent
        fields = [
            'title', 'description', 'event_type', 'location', 
            'start_time', 'end_time', 'max_participants', 'online_link', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Event description...'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event location or online platform'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'online_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://meet.google.com/...'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "End time must be after start time."
            )
        
        return cleaned_data 