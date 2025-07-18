from django import forms
from .models import Resource, ResourceComment, ResourceCollection


class ResourceForm(forms.ModelForm):
    """Form for creating and editing resources."""
    
    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'resource_type', 'category', 
            'community', 'file', 'external_link', 'tags', 'course_code', 
            'academic_year', 'is_public', 'requires_approval'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter resource title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the resource...'
            }),
            'resource_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'community': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'external_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CS101, MATH201'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2023-2024'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_approval': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        external_link = cleaned_data.get('external_link')
        resource_type = cleaned_data.get('resource_type')
        
        # Validate that either file or external link is provided
        if not file and not external_link:
            raise forms.ValidationError(
                "Either a file or external link must be provided."
            )
        
        # Validate file upload for file-type resources
        if resource_type == 'file' and not file:
            raise forms.ValidationError(
                "A file must be uploaded for file-type resources."
            )
        
        # Validate external link for link-type resources
        if resource_type == 'link' and not external_link:
            raise forms.ValidationError(
                "An external link must be provided for link-type resources."
            )
        
        return cleaned_data


class ResourceCommentForm(forms.ModelForm):
    """Form for adding comments to resources."""
    
    class Meta:
        model = ResourceComment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make rating optional
        self.fields['rating'].required = False


class ResourceCollectionForm(forms.ModelForm):
    """Form for creating and editing resource collections."""
    
    class Meta:
        model = ResourceCollection
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter collection name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your collection...'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        } 