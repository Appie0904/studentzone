from django.db import models
from django.contrib.auth.models import User
from communities.models import Community
from core.models import StudyField
from django.utils import timezone
import os


class ResourceCategory(models.Model):
    """Categories for organizing resources"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE, related_name='resource_categories')
    
    class Meta:
        verbose_name_plural = "Resource Categories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.study_field.name})"


class Resource(models.Model):
    """Educational resources shared by students"""
    RESOURCE_TYPE_CHOICES = [
        ('lecture_notes', 'Lecture Notes'),
        ('slides', 'Presentation Slides'),
        ('code', 'Code Samples'),
        ('book_summary', 'Book Summary'),
        ('study_guide', 'Study Guide'),
        ('exam_prep', 'Exam Preparation'),
        ('assignment', 'Assignment'),
        ('research_paper', 'Research Paper'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='resources')
    
    # File information
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True, help_text="File size in bytes")
    external_link = models.URLField(blank=True, help_text="Link to external resource")
    
    # Content details
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    course_code = models.CharField(max_length=20, blank=True, help_text="e.g., CS101, MATH201")
    academic_year = models.CharField(max_length=20, blank=True, help_text="e.g., 2023-2024")
    
    # Author and ownership
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    is_anonymous = models.BooleanField(default=False)
    
    # Visibility and access
    is_public = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Engagement metrics
    download_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('resources:resource_detail', kwargs={'pk': self.pk})
    
    def get_vote_score(self):
        return self.upvotes - self.downvotes
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return None
    
    def get_file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0


class ResourceVote(models.Model):
    """Voting system for resources"""
    VOTE_TYPE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_votes')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.vote_type} on {self.resource.title}"


class ResourceDownload(models.Model):
    """Track resource downloads"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_downloads')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} downloaded {self.resource.title}"


class ResourceComment(models.Model):
    """Comments and reviews on resources"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_comments')
    content = models.TextField()
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        null=True, blank=True,
        help_text="Rating from 1 to 5 stars"
    )
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.resource.title}"


class ResourceBookmark(models.Model):
    """User bookmarks for resources"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this resource")
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"


class ResourceCollection(models.Model):
    """Collections of resources created by users"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_collections')
    resources = models.ManyToManyField(Resource, related_name='collections')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} by {self.creator.username}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('resources:collection_detail', kwargs={'pk': self.pk})


class ResourceReport(models.Model):
    """Reports for inappropriate or problematic resources"""
    REASON_CHOICES = [
        ('copyright', 'Copyright Violation'),
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('low_quality', 'Low Quality'),
        ('wrong_category', 'Wrong Category'),
        ('other', 'Other'),
    ]
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_reports')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(help_text="Additional details about the issue")
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_reports')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report on {self.resource.title} by {self.reporter.username}"
