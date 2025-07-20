from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.models import User
from .models import (
    Resource, ResourceCategory, ResourceVote, ResourceDownload,
    ResourceComment, ResourceBookmark, ResourceCollection, ResourceReport
)
from .forms import ResourceForm, ResourceCommentForm, ResourceCollectionForm


def resource_list(request):
    """List all resources with filtering and search."""
    resources = Resource.objects.select_related('author', 'category', 'category__study_field').prefetch_related('votes')
    
    # Search
    query = request.GET.get('q')
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        resources = resources.filter(category_id=category_id)
    
    # Filter by study field
    field_id = request.GET.get('field')
    if field_id:
        resources = resources.filter(category__study_field_id=field_id)
    
    # Filter by type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'popular':
        resources = resources.annotate(vote_count=Count('votes')).order_by('-vote_count', '-created_at')
    elif sort == 'downloads':
        resources = resources.annotate(download_count=Count('downloads')).order_by('-download_count', '-created_at')
    else:
        resources = resources.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and fields for filters
    categories = ResourceCategory.objects.all()
    from core.models import StudyField
    study_fields = StudyField.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'study_fields': study_fields,
        'current_filters': {
            'q': query,
            'category': category_id,
            'field': field_id,
            'type': resource_type,
            'sort': sort,
        }
    }
    return render(request, 'resources/resource_list.html', context)


@login_required
def resource_upload(request):
    """Upload a new resource."""
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.save()
            messages.success(request, 'Resource uploaded successfully!')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    
    context = {
        'form': form,
        'title': 'Upload Resource'
    }
    return render(request, 'resources/resource_form.html', context)


def resource_detail(request, pk):
    """View a specific resource."""
    resource = get_object_or_404(Resource.objects.select_related('author', 'category', 'category__study_field'), pk=pk)
    
    # Track view if user is authenticated
    if request.user.is_authenticated:
        ResourceDownload.objects.get_or_create(
            user=request.user,
            resource=resource
        )
    
    # Get comments
    comments = resource.comments.select_related('author').order_by('-created_at')
    
    # Check if user has bookmarked this resource
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = ResourceBookmark.objects.filter(user=request.user, resource=resource).exists()
    
    # Get related resources
    related_resources = Resource.objects.filter(
        Q(category=resource.category) | Q(category__study_field=resource.category.study_field)
    ).exclude(pk=resource.pk)[:6]
    
    context = {
        'resource': resource,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'related_resources': related_resources,
        'comment_form': ResourceCommentForm()
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def resource_edit(request, pk):
    """Edit a resource."""
    resource = get_object_or_404(Resource, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(instance=resource)
    
    context = {
        'form': form,
        'resource': resource,
        'title': 'Edit Resource'
    }
    return render(request, 'resources/resource_form.html', context)


@login_required
def resource_delete(request, pk):
    """Delete a resource."""
    resource = get_object_or_404(Resource, pk=pk, author=request.user)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully!')
        return redirect('resources:resource_list')
    
    context = {
        'resource': resource
    }
    return render(request, 'resources/resource_confirm_delete.html', context)


@login_required
def resource_download(request, pk):
    """Download a resource."""
    resource = get_object_or_404(Resource, pk=pk)
    
    # Record download
    ResourceDownload.objects.create(
        user=request.user,
        resource=resource
    )
    
    # Redirect to file or external link
    if resource.file:
        # In production, you'd want to serve files securely
        return redirect(resource.file.url)
    elif resource.external_link:
        return redirect(resource.external_link)
    else:
        messages.error(request, 'No file or link available for download.')
        return redirect('resources:resource_detail', pk=resource.pk)


@login_required
def resource_vote(request, pk):
    """Vote on a resource."""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        resource = get_object_or_404(Resource, pk=pk)
        vote_type = request.POST.get('vote_type')
        
        if vote_type not in ['upvote', 'downvote']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)
        
        # Check if user already voted
        existing_vote = ResourceVote.objects.filter(user=request.user, resource=resource).first()
        
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Remove vote
                existing_vote.delete()
                action = 'removed'
            else:
                # Change vote
                existing_vote.vote_type = vote_type
                existing_vote.save()
                action = 'changed'
        else:
            # Create new vote
            ResourceVote.objects.create(
                user=request.user,
                resource=resource,
                vote_type=vote_type
            )
            action = 'added'
        
        # Get updated vote counts
        upvotes = resource.votes.filter(vote_type='upvote').count()
        downvotes = resource.votes.filter(vote_type='downvote').count()
        
        return JsonResponse({
            'success': True,
            'action': action,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'score': upvotes - downvotes
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def resource_comment_create(request, pk):
    """Add a comment to a resource."""
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == 'POST':
        form = ResourceCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.resource = resource
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('resources:resource_detail', pk=resource.pk)


@login_required
def resource_comment_edit(request, pk, comment_pk):
    """Edit a resource comment."""
    comment = get_object_or_404(ResourceComment, pk=comment_pk, author=request.user)
    
    if request.method == 'POST':
        form = ResourceCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('resources:resource_detail', pk=pk)
    else:
        form = ResourceCommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'resource': comment.resource
    }
    return render(request, 'resources/comment_form.html', context)


@login_required
def resource_comment_delete(request, pk, comment_pk):
    """Delete a resource comment."""
    comment = get_object_or_404(ResourceComment, pk=comment_pk, author=request.user)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('resources:resource_detail', pk=pk)
    
    context = {
        'comment': comment,
        'resource': comment.resource
    }
    return render(request, 'resources/comment_confirm_delete.html', context)


@login_required
def resource_bookmark(request, pk):
    """Bookmark/unbookmark a resource."""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        resource = get_object_or_404(Resource, pk=pk)
        
        bookmark, created = ResourceBookmark.objects.get_or_create(
            user=request.user,
            resource=resource
        )
        
        if not created:
            bookmark.delete()
            action = 'removed'
        else:
            action = 'added'
        
        return JsonResponse({
            'success': True,
            'action': action,
            'is_bookmarked': action == 'added'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def bookmark_list(request):
    """List user's bookmarked resources."""
    bookmarks = ResourceBookmark.objects.filter(user=request.user).select_related('resource', 'resource__author', 'resource__category', 'resource__category__study_field')
    
    # Pagination
    paginator = Paginator(bookmarks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookmarks': bookmarks,
        'title': 'My Resource Bookmarks'
    }
    return render(request, 'resources/bookmark_list.html', context)


@login_required
def collection_list(request):
    """List user's resource collections."""
    collections = ResourceCollection.objects.filter(creator=request.user).prefetch_related('resources')
    
    context = {
        'collections': collections,
        'title': 'My Collections'
    }
    return render(request, 'resources/collection_list.html', context)


@login_required
def collection_create(request):
    """Create a new resource collection."""
    if request.method == 'POST':
        form = ResourceCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user
            collection.save()
            messages.success(request, 'Collection created successfully!')
            return redirect('resources:collection_detail', pk=collection.pk)
    else:
        form = ResourceCollectionForm()
    
    context = {
        'form': form,
        'title': 'Create Collection'
    }
    return render(request, 'resources/collection_form.html', context)


def collection_detail(request, pk):
    """View a resource collection."""
    collection = get_object_or_404(ResourceCollection.objects.select_related('creator'), pk=pk)
    
    # Check if user can edit
    can_edit = request.user == collection.creator
    
    context = {
        'collection': collection,
        'can_edit': can_edit
    }
    return render(request, 'resources/collection_detail.html', context)


@login_required
def collection_edit(request, pk):
    """Edit a resource collection."""
    collection = get_object_or_404(ResourceCollection, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        form = ResourceCollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection updated successfully!')
            return redirect('resources:collection_detail', pk=collection.pk)
    else:
        form = ResourceCollectionForm(instance=collection)
    
    context = {
        'form': form,
        'collection': collection,
        'title': 'Edit Collection'
    }
    return render(request, 'resources/collection_form.html', context)


@login_required
def collection_delete(request, pk):
    """Delete a resource collection."""
    collection = get_object_or_404(ResourceCollection, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        collection.delete()
        messages.success(request, 'Collection deleted successfully!')
        return redirect('resources:collection_list')
    
    context = {
        'collection': collection
    }
    return render(request, 'resources/collection_confirm_delete.html', context)


@login_required
def collection_add_resource(request, pk, resource_pk):
    """Add a resource to a collection."""
    collection = get_object_or_404(ResourceCollection, pk=pk, creator=request.user)
    resource = get_object_or_404(Resource, pk=resource_pk)
    
    if resource not in collection.resources.all():
        collection.resources.add(resource)
        messages.success(request, f'Added "{resource.title}" to collection.')
    else:
        messages.info(request, 'Resource is already in this collection.')
    
    return redirect('resources:resource_detail', pk=resource_pk)


@login_required
def collection_remove_resource(request, pk, resource_pk):
    """Remove a resource from a collection."""
    collection = get_object_or_404(ResourceCollection, pk=pk, creator=request.user)
    resource = get_object_or_404(Resource, pk=resource_pk)
    
    collection.resources.remove(resource)
    messages.success(request, f'Removed "{resource.title}" from collection.')
    
    return redirect('resources:collection_detail', pk=collection.pk)


@login_required
def resource_report(request, pk):
    """Report a resource."""
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        if reason:
            ResourceReport.objects.create(
                reporter=request.user,
                resource=resource,
                reason=reason,
                description=description
            )
            messages.success(request, 'Resource reported successfully. Thank you for helping keep our community safe.')
            return redirect('resources:resource_detail', pk=resource.pk)
        else:
            messages.error(request, 'Please select a reason for reporting.')
    
    context = {
        'resource': resource,
        'report_reasons': ResourceReport.REASON_CHOICES
    }
    return render(request, 'resources/resource_report.html', context)


def resource_by_category(request, category_id):
    """List resources by category."""
    category = get_object_or_404(ResourceCategory, pk=category_id)
    resources = Resource.objects.filter(category=category).select_related('author', 'category', 'category__study_field').prefetch_related('votes')
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, 'resources/resource_by_category.html', context)


def resource_by_field(request, field_id):
    """List resources by study field."""
    from core.models import StudyField
    study_field = get_object_or_404(StudyField, pk=field_id)
    resources = Resource.objects.filter(category__study_field=study_field).select_related('author', 'category', 'category__study_field').prefetch_related('votes')
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'study_field': study_field,
        'page_obj': page_obj
    }
    return render(request, 'resources/resource_by_field.html', context)
