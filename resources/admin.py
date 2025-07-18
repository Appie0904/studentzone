from django.contrib import admin
from .models import ResourceCategory, Resource, ResourceVote, ResourceDownload, ResourceComment, ResourceBookmark, ResourceCollection, ResourceReport


class ResourceVoteInline(admin.TabularInline):
    model = ResourceVote
    extra = 1


class ResourceCommentInline(admin.TabularInline):
    model = ResourceComment
    extra = 1


class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_field', 'parent_category', 'icon']
    list_filter = ['study_field', 'parent_category']
    search_fields = ['name', 'description']
    ordering = ['name']


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'resource_type', 'category', 'community', 'download_count', 'view_count', 'is_approved', 'created_at']
    list_filter = ['resource_type', 'is_public', 'is_approved', 'requires_approval', 'created_at', 'community']
    search_fields = ['title', 'description', 'author__username', 'tags', 'course_code']
    ordering = ['-created_at']
    inlines = [ResourceVoteInline, ResourceCommentInline]
    readonly_fields = ['download_count', 'view_count', 'upvotes', 'downvotes', 'file_size']


class ResourceVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'resource__title']
    ordering = ['-created_at']


class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'downloaded_at', 'ip_address']
    list_filter = ['downloaded_at', 'resource__resource_type']
    search_fields = ['user__username', 'resource__title']
    ordering = ['-downloaded_at']


class ResourceCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'resource', 'rating', 'is_anonymous', 'created_at']
    list_filter = ['rating', 'is_anonymous', 'created_at', 'resource__resource_type']
    search_fields = ['content', 'author__username', 'resource__title']
    ordering = ['-created_at']


class ResourceBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
    list_filter = ['created_at', 'resource__resource_type']
    search_fields = ['user__username', 'resource__title', 'notes']
    ordering = ['-created_at']


class ResourceCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description', 'creator__username']
    ordering = ['-created_at']


class ResourceReportAdmin(admin.ModelAdmin):
    list_display = ['resource', 'reporter', 'reason', 'is_resolved', 'created_at', 'resolved_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['reporter__username', 'resource__title', 'description']
    ordering = ['-created_at']


admin.site.register(ResourceCategory, ResourceCategoryAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceVote, ResourceVoteAdmin)
admin.site.register(ResourceDownload, ResourceDownloadAdmin)
admin.site.register(ResourceComment, ResourceCommentAdmin)
admin.site.register(ResourceBookmark, ResourceBookmarkAdmin)
admin.site.register(ResourceCollection, ResourceCollectionAdmin)
admin.site.register(ResourceReport, ResourceReportAdmin)
