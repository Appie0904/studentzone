from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import University, StudyField, UserProfile, Badge, UserBadge


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'city', 'website']
    list_filter = ['city']
    search_fields = ['name', 'abbreviation', 'city']
    ordering = ['name']


class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_field', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent_field']
    search_fields = ['name', 'description']
    ordering = ['name']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'study_field', 'study_level', 'reputation_score', 'is_verified']
    list_filter = ['university', 'study_field', 'study_level', 'is_verified']
    search_fields = ['user__username', 'user__email', 'bio']
    ordering = ['-reputation_score']


class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['color', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    list_filter = ['badge', 'awarded_at']
    search_fields = ['user__username', 'badge__name']
    ordering = ['-awarded_at']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(University, UniversityAdmin)
admin.site.register(StudyField, StudyFieldAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
