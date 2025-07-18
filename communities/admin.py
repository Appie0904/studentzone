from django.contrib import admin
from .models import Community, CommunityMembership, CommunityInvitation, CommunityEvent, EventParticipant


class CommunityMembershipInline(admin.TabularInline):
    model = CommunityMembership
    extra = 1


class CommunityEventInline(admin.TabularInline):
    model = CommunityEvent
    extra = 1


class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_field', 'created_by', 'member_count', 'is_active', 'created_at']
    list_filter = ['study_field', 'is_active', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    ordering = ['name']
    inlines = [CommunityMembershipInline, CommunityEventInline]


class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'role', 'joined_at', 'is_active']
    list_filter = ['role', 'is_active', 'joined_at', 'community']
    search_fields = ['user__username', 'community__name']
    ordering = ['-joined_at']


class CommunityInvitationAdmin(admin.ModelAdmin):
    list_display = ['community', 'invited_user', 'invited_by', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'created_at', 'community']
    search_fields = ['invited_user__username', 'invited_by__username', 'community__name']
    ordering = ['-created_at']


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 1


class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'community', 'event_type', 'start_time', 'end_time', 'created_by', 'is_public']
    list_filter = ['event_type', 'is_public', 'start_time', 'community']
    search_fields = ['title', 'description', 'created_by__username']
    ordering = ['-start_time']
    inlines = [EventParticipantInline]


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'registered_at']
    list_filter = ['status', 'registered_at', 'event__event_type']
    search_fields = ['user__username', 'event__title']
    ordering = ['-registered_at']


admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMembership, CommunityMembershipAdmin)
admin.site.register(CommunityInvitation, CommunityInvitationAdmin)
admin.site.register(CommunityEvent, CommunityEventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
