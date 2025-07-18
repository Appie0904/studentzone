from django.contrib import admin
from .models import Discussion, Comment, Vote, DiscussionView, DiscussionBookmark, DiscussionNotification


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'community', 'discussion_type', 'is_pinned', 'is_closed', 'view_count', 'created_at']
    list_filter = ['discussion_type', 'is_pinned', 'is_closed', 'is_anonymous', 'created_at', 'community']
    search_fields = ['title', 'content', 'author__username', 'tags']
    ordering = ['-created_at']
    inlines = [CommentInline]
    readonly_fields = ['view_count', 'upvotes', 'downvotes']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'discussion', 'is_solution', 'upvotes', 'downvotes', 'created_at']
    list_filter = ['is_solution', 'is_anonymous', 'created_at', 'discussion__discussion_type']
    search_fields = ['content', 'author__username', 'discussion__title']
    ordering = ['-created_at']
    readonly_fields = ['upvotes', 'downvotes']


class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'vote_type', 'content_type', 'object_id', 'created_at']
    list_filter = ['vote_type', 'created_at', 'content_type']
    search_fields = ['user__username']
    ordering = ['-created_at']


class DiscussionViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'discussion', 'viewed_at', 'ip_address']
    list_filter = ['viewed_at', 'discussion__discussion_type']
    search_fields = ['user__username', 'discussion__title']
    ordering = ['-viewed_at']


class DiscussionBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'discussion', 'created_at']
    list_filter = ['created_at', 'discussion__discussion_type']
    search_fields = ['user__username', 'discussion__title', 'notes']
    ordering = ['-created_at']


class DiscussionNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'discussion', 'from_user', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'discussion__title', 'from_user__username']
    ordering = ['-created_at']


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(DiscussionView, DiscussionViewAdmin)
admin.site.register(DiscussionBookmark, DiscussionBookmarkAdmin)
admin.site.register(DiscussionNotification, DiscussionNotificationAdmin)
