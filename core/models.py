from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class University(models.Model):
    """Dutch universities and institutions"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="SAML organization code (e.g., tudelft.nl)")
    abbreviation = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class StudyField(models.Model):
    """Academic disciplines and fields of study"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parent_field = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subfields')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for students"""
    STUDY_LEVEL_CHOICES = [
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('alumni', 'Alumni'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    study_field = models.ForeignKey(StudyField, on_delete=models.SET_NULL, null=True, blank=True)
    study_level = models.CharField(max_length=20, choices=STUDY_LEVEL_CHOICES, blank=True)
    graduation_year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2030)],
        blank=True, null=True
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation_score = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    # Contact preferences
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.university.abbreviation if self.university else 'No University'}"
    
    def get_reputation_badge(self):
        """Return reputation badge based on score"""
        if self.reputation_score >= 1000:
            return "Legend"
        elif self.reputation_score >= 500:
            return "Expert"
        elif self.reputation_score >= 100:
            return "Helper"
        elif self.reputation_score >= 50:
            return "Contributor"
        else:
            return "Newcomer"


class Badge(models.Model):
    """Achievement badges for users"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # FontAwesome icon class
    color = models.CharField(max_length=20, default='primary')
    criteria = models.TextField(help_text="What users need to do to earn this badge")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """User badge assignments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
