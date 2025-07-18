from django.db import models
from django.contrib.auth.models import User
from communities.models import Community
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Discussion(models.Model):
    """Base discussion model for questions and topics"""
    DISCUSSION_TYPE_CHOICES = [
        ('question', 'Question'),
        ('discussion', 'Discussion'),
        ('announcement', 'Announcement'),
        ('resource_share', 'Resource Share'),
    ]
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    discussion_type = models.CharField(max_length=20, choices=DISCUSSION_TYPE_CHOICES, default='discussion')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    
    # Status and visibility
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    
    # Engagement metrics
    view_count = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Tags for categorization
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    class Meta:
        ordering = ['-is_pinned', '-last_activity']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('discussions:discussion_detail', kwargs={'pk': self.pk})
    
    def get_vote_score(self):
        return self.upvotes - self.downvotes
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Comment(models.Model):
    """Comments on discussions"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Status
    is_solution = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    
    # Engagement
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.discussion.title[:50]}"
    
    def get_vote_score(self):
        return self.upvotes - self.downvotes


class Vote(models.Model):
    """Voting system for discussions and comments"""
    VOTE_TYPE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key to either Discussion or Comment
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.vote_type} on {self.content_type.model}"


class DiscussionView(models.Model):
    """Track discussion views"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_discussions')
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        unique_together = ['discussion', 'user']
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} viewed {self.discussion.title}"


class DiscussionBookmark(models.Model):
    """User bookmarks for discussions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this discussion")
    
    class Meta:
        unique_together = ['user', 'discussion']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.discussion.title}"


class DiscussionNotification(models.Model):
    """Notifications for discussion activity"""
    NOTIFICATION_TYPE_CHOICES = [
        ('new_comment', 'New Comment'),
        ('reply', 'Reply to Comment'),
        ('solution_marked', 'Solution Marked'),
        ('mention', 'Mentioned in Comment'),
        ('upvote', 'Received Upvote'),
        ('downvote', 'Received Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='notifications')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    # Status
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"
