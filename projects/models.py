from django.db import models
from django.contrib.auth.models import User
from communities.models import Community
from core.models import StudyField, University
from django.utils import timezone


class Project(models.Model):
    """Cross-institution projects for collaboration"""
    PROJECT_TYPE_CHOICES = [
        ('research', 'Research Project'),
        ('coursework', 'Coursework'),
        ('hackathon', 'Hackathon'),
        ('startup', 'Startup/Business'),
        ('open_source', 'Open Source'),
        ('competition', 'Competition'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('recruiting', 'Recruiting'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    # Project details
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='projects')
    study_fields = models.ManyToManyField(StudyField, related_name='projects')
    universities = models.ManyToManyField(University, related_name='projects')
    
    # Team and collaboration
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    team_size_min = models.IntegerField(default=1)
    team_size_max = models.IntegerField(null=True, blank=True)
    is_open_to_all = models.BooleanField(default=True)
    
    # Timeline
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    # Contact and communication
    contact_email = models.EmailField(blank=True)
    external_link = models.URLField(blank=True)
    meeting_schedule = models.TextField(blank=True)
    
    # Visibility and engagement
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    application_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('projects:project_detail', kwargs={'pk': self.pk})
    
    def is_recruiting(self):
        return self.status == 'recruiting' and self.application_count < (self.team_size_max or float('inf'))
    
    def get_team_members(self):
        return self.memberships.filter(role='member').select_related('user')


class ProjectMembership(models.Model):
    """Team membership in projects"""
    ROLE_CHOICES = [
        ('leader', 'Project Leader'),
        ('member', 'Team Member'),
        ('mentor', 'Mentor'),
        ('advisor', 'Advisor'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Contribution tracking
    contribution_description = models.TextField(blank=True)
    hours_contributed = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['project', 'user']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"


class ProjectApplication(models.Model):
    """Applications to join projects"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Application details
    motivation = models.TextField()
    relevant_experience = models.TextField()
    time_commitment = models.CharField(max_length=100, help_text="e.g., 10 hours/week")
    skills = models.TextField(help_text="Relevant skills and expertise")
    
    # Contact preferences
    preferred_contact = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('discord', 'Discord'),
        ('slack', 'Slack'),
        ('other', 'Other'),
    ], default='email')
    contact_info = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    
    class Meta:
        unique_together = ['project', 'applicant']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.username} applied to {self.project.title}"


class StudyPartner(models.Model):
    """Study partner matching system"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_partner_profile')
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE, related_name='study_partners')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='study_partners')
    
    # Preferences
    preferred_study_methods = models.CharField(max_length=500, blank=True, help_text="e.g., group study, online, library")
    subjects_of_interest = models.TextField(help_text="Specific subjects or topics you want to study")
    availability = models.TextField(help_text="When you're available to study")
    
    # Partner preferences
    preferred_universities = models.ManyToManyField(University, blank=True, related_name='preferred_by_partners')
    max_distance_km = models.IntegerField(default=50, help_text="Maximum distance for in-person meetings")
    online_only = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'study_field', 'university']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.study_field.name} at {self.university.abbreviation}"


class StudyPartnerRequest(models.Model):
    """Study partner connection requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_partner_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partner_requests')
    study_field = models.ForeignKey(StudyField, on_delete=models.CASCADE)
    
    # Request details
    message = models.TextField()
    proposed_meeting_time = models.DateTimeField(null=True, blank=True)
    meeting_location = models.CharField(max_length=200, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['requester', 'recipient', 'study_field']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.requester.username} → {self.recipient.username} for {self.study_field.name}"
