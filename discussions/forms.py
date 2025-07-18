from django import forms
from .models import Discussion, Comment


class DiscussionForm(forms.ModelForm):
    """Form for creating and editing discussions."""
    
    class Meta:
        model = Discussion
        fields = [
            'title', 'content', 'discussion_type', 'community', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter discussion title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your discussion content...'
            }),
            'discussion_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'community': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter communities to only show those the user is a member of
            from communities.models import CommunityMembership
            user_communities = CommunityMembership.objects.filter(
                user=user, 
                status='accepted'
            ).values_list('community_id', flat=True)
            self.fields['community'].queryset = self.fields['community'].queryset.filter(
                id__in=user_communities
            )


class CommentForm(forms.ModelForm):
    """Form for adding comments to discussions."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            })
        } 