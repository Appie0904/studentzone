from django.db import models
from django.contrib.auth.models import User
from core.models import StudyField, University
from django.utils import timezone


class Community(models.Model):
    """Field-based communities for students"""
    name = models.CharField(max_length=200)
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE, related_name='communities')
    description = models.TextField()
    rules = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_communities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Community stats
    member_count = models.IntegerField(default=0)
    discussion_count = models.IntegerField(default=0)
    resource_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Communities"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.study_field.name})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('communities:community_detail', kwargs={'pk': self.pk})


class CommunityMembership(models.Model):
    """User membership in communities"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_memberships')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'community']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.community.name} ({self.role})"


class CommunityInvitation(models.Model):
    """Invitations to join communities"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]
    
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['community', 'invited_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invitation to {self.community.name} for {self.invited_user.username}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class CommunityEvent(models.Model):
    """Events organized by communities"""
    EVENT_TYPE_CHOICES = [
        ('study_session', 'Study Session'),
        ('workshop', 'Workshop'),
        ('lecture', 'Guest Lecture'),
        ('hackathon', 'Hackathon'),
        ('meetup', 'Meetup'),
        ('other', 'Other'),
    ]
    
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    online_link = models.URLField(blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} - {self.community.name}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('communities:event_detail', kwargs={'pk': self.pk})


class EventParticipant(models.Model):
    """Event participation tracking"""
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    status = models.CharField(max_length=20, choices=[
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ], default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
