from django.contrib import admin
from .models import Project, ProjectMembership, ProjectApplication, StudyPartner, StudyPartnerRequest


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 1


class ProjectApplicationInline(admin.TabularInline):
    model = ProjectApplication
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'project_type', 'status', 'team_size_min', 'team_size_max', 'is_featured', 'created_at']
    list_filter = ['project_type', 'status', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'creator__username']
    ordering = ['-created_at']
    inlines = [ProjectMembershipInline, ProjectApplicationInline]
    readonly_fields = ['view_count', 'application_count']


class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'joined_at', 'is_active', 'hours_contributed']
    list_filter = ['role', 'is_active', 'joined_at', 'project__project_type']
    search_fields = ['user__username', 'project__title']
    ordering = ['-joined_at']


class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'project', 'status', 'applied_at', 'reviewed_at', 'reviewed_by']
    list_filter = ['status', 'applied_at', 'preferred_contact', 'project__project_type']
    search_fields = ['applicant__username', 'project__title', 'motivation']
    ordering = ['-applied_at']


class StudyPartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'study_field', 'university', 'is_active', 'online_only', 'created_at']
    list_filter = ['study_field', 'university', 'is_active', 'online_only', 'created_at']
    search_fields = ['user__username', 'subjects_of_interest', 'preferred_study_methods']
    ordering = ['-created_at']


class StudyPartnerRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'recipient', 'study_field', 'status', 'created_at', 'responded_at']
    list_filter = ['status', 'created_at', 'study_field']
    search_fields = ['requester__username', 'recipient__username', 'message']
    ordering = ['-created_at']


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMembership, ProjectMembershipAdmin)
admin.site.register(ProjectApplication, ProjectApplicationAdmin)
admin.site.register(StudyPartner, StudyPartnerAdmin)
admin.site.register(StudyPartnerRequest, StudyPartnerRequestAdmin)
