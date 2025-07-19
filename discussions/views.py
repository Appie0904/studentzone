from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Discussion, Comment, Vote, DiscussionBookmark
from .forms import DiscussionForm, CommentForm
from communities.models import Community
from django.contrib.contenttypes.models import ContentType
from .models import DiscussionView


def discussion_list(request):
    """List all discussions"""
    discussions = Discussion.objects.all().order_by('-created_at')
    
    # Filter by community
    community_id = request.GET.get('community')
    if community_id:
        discussions = discussions.filter(community_id=community_id)
    
    # Filter by type
    discussion_type = request.GET.get('type')
    if discussion_type:
        discussions = discussions.filter(discussion_type=discussion_type)
    
    # Search
    search = request.GET.get('search')
    if search:
        discussions = discussions.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(discussions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    communities = Community.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'communities': communities,
        'selected_community': community_id,
        'selected_type': discussion_type,
        'search': search,
    }
    
    return render(request, 'discussions/discussion_list.html', context)


@login_required
def discussion_create(request):
    """Create a new discussion"""
    if request.method == 'POST':
        form = DiscussionForm(request.POST, user=request.user)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            
            messages.success(request, 'Discussion created successfully!')
            return redirect('discussions:discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Create Discussion'
    }
    
    return render(request, 'discussions/discussion_form.html', context)


def discussion_detail(request, pk):
    """View discussion details"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    # Increment view count
    if request.user.is_authenticated:
        DiscussionView.objects.get_or_create(
            discussion=discussion,
            user=request.user,
            defaults={'ip_address': request.META.get('REMOTE_ADDR')}
        )
        discussion.view_count += 1
        discussion.save()
    
    # Get comments
    comments = discussion.comments.filter(parent_comment=None).order_by('created_at')
    
    # Check if user has bookmarked
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = discussion.bookmarked_by.filter(user=request.user).exists()
    
    context = {
        'discussion': discussion,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
    }
    
    return render(request, 'discussions/discussion_detail.html', context)


@login_required
def discussion_edit(request, pk):
    """Edit discussion"""
    discussion = get_object_or_404(Discussion, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion updated successfully!')
            return redirect('discussions:discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion, user=request.user)
    
    context = {
        'form': form,
        'discussion': discussion,
        'title': 'Edit Discussion'
    }
    
    return render(request, 'discussions/discussion_form.html', context)


@login_required
def discussion_delete(request, pk):
    """Delete discussion"""
    discussion = get_object_or_404(Discussion, pk=pk, author=request.user)
    
    if request.method == 'POST':
        discussion.delete()
        messages.success(request, 'Discussion deleted successfully!')
        return redirect('discussions:discussion_list')
    
    return render(request, 'discussions/discussion_confirm_delete.html', {'discussion': discussion})


@login_required
def discussion_pin(request, pk):
    """Pin/unpin discussion"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    # Check if user has permission
    try:
        membership = discussion.community.memberships.get(user=request.user, is_active=True)
        if membership.role not in ['admin', 'moderator']:
            messages.error(request, 'You do not have permission to pin discussions.')
            return redirect('discussions:discussion_detail', pk=discussion.pk)
    except:
        messages.error(request, 'You do not have permission to pin discussions.')
        return redirect('discussions:discussion_detail', pk=discussion.pk)
    
    if request.method == 'POST':
        discussion.is_pinned = not discussion.is_pinned
        discussion.save()
        
        action = 'pinned' if discussion.is_pinned else 'unpinned'
        messages.success(request, f'Discussion {action} successfully!')
    
    return redirect('discussions:discussion_detail', pk=discussion.pk)


@login_required
def discussion_close(request, pk):
    """Close/open discussion"""
    discussion = get_object_or_404(Discussion, pk=pk, author=request.user)
    
    if request.method == 'POST':
        discussion.is_closed = not discussion.is_closed
        discussion.save()
        
        action = 'closed' if discussion.is_closed else 'reopened'
        messages.success(request, f'Discussion {action} successfully!')
    
    return redirect('discussions:discussion_detail', pk=discussion.pk)


# Comment views
@login_required
def comment_create(request, discussion_pk):
    """Create a comment"""
    print(f"DEBUG: comment_create view called with discussion_pk: {discussion_pk}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
    
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    print(f"DEBUG: Discussion found: {discussion.title}")
    
    if request.method == 'POST':
        print(f"DEBUG: Comment creation POST request received")
        print(f"DEBUG: POST data: {request.POST}")
        
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment')
        
        print(f"DEBUG: Content: {content}")
        print(f"DEBUG: Parent comment ID: {parent_comment_id}")
        
        if content and content.strip():
            try:
                comment = Comment.objects.create(
                    discussion=discussion,
                    content=content.strip(),
                    author=request.user
                )
                
                if parent_comment_id:
                    comment.parent_comment_id = parent_comment_id
                    comment.save()
                
                print(f"DEBUG: Comment created successfully with ID: {comment.pk}")
                messages.success(request, 'Comment added successfully!')
            except Exception as e:
                print(f"DEBUG: Error creating comment: {e}")
                messages.error(request, f'Error creating comment: {str(e)}')
        else:
            print(f"DEBUG: No content provided")
            messages.error(request, 'Please enter a comment.')
    else:
        print(f"DEBUG: Non-POST request to comment_create")
    
    return redirect('discussions:discussion_detail', pk=discussion.pk)


@login_required
def comment_edit(request, pk):
    """Edit comment"""
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    
    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        
        messages.success(request, 'Comment updated successfully!')
        return redirect('discussions:discussion_detail', pk=comment.discussion.pk)
    
    return render(request, 'discussions/comment_form.html', {'comment': comment})


@login_required
def comment_delete(request, pk):
    """Delete comment"""
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    
    if request.method == 'POST':
        discussion_pk = comment.discussion.pk
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('discussions:discussion_detail', pk=discussion_pk)
    
    return render(request, 'discussions/comment_confirm_delete.html', {'comment': comment})


@login_required
def comment_solution(request, pk):
    """Mark comment as solution"""
    comment = get_object_or_404(Comment, pk=pk)
    discussion = comment.discussion
    
    # Check if user is the discussion author
    if request.user != discussion.author:
        messages.error(request, 'Only the discussion author can mark solutions.')
        return redirect('discussions:discussion_detail', pk=discussion.pk)
    
    if request.method == 'POST':
        # Remove solution from other comments
        discussion.comments.update(is_solution=False)
        
        # Mark this comment as solution
        comment.is_solution = True
        comment.save()
        
        messages.success(request, 'Solution marked successfully!')
    
    return redirect('discussions:discussion_detail', pk=discussion.pk)


# Voting views
@login_required
def discussion_upvote(request, pk):
    """Upvote discussion"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if request.method == 'POST':
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Discussion),
            object_id=discussion.pk,
            defaults={'vote_type': 'upvote'}
        )
        
        if not created:
            if vote.vote_type == 'upvote':
                vote.delete()
                discussion.upvotes -= 1
            else:
                vote.vote_type = 'upvote'
                vote.save()
                discussion.downvotes -= 1
                discussion.upvotes += 1
        else:
            discussion.upvotes += 1
        
        discussion.save()
        
        return JsonResponse({
            'success': True,
            'vote_count': discussion.upvotes - discussion.downvotes,
            'user_vote': 'upvote' if created else None
        })
    
    return JsonResponse({'success': False})


@login_required
def discussion_downvote(request, pk):
    """Downvote discussion"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if request.method == 'POST':
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Discussion),
            object_id=discussion.pk,
            defaults={'vote_type': 'downvote'}
        )
        
        if not created:
            if vote.vote_type == 'downvote':
                vote.delete()
                discussion.downvotes -= 1
            else:
                vote.vote_type = 'downvote'
                vote.save()
                discussion.upvotes -= 1
                discussion.downvotes += 1
        else:
            discussion.downvotes += 1
        
        discussion.save()
        
        return JsonResponse({
            'success': True,
            'vote_count': discussion.upvotes - discussion.downvotes,
            'user_vote': 'downvote' if created else None
        })
    
    return JsonResponse({'success': False})


@login_required
def comment_upvote(request, pk):
    """Upvote comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=comment.pk,
            defaults={'vote_type': 'upvote'}
        )
        
        if not created:
            if vote.vote_type == 'upvote':
                vote.delete()
                comment.upvotes -= 1
            else:
                vote.vote_type = 'upvote'
                vote.save()
                comment.downvotes -= 1
                comment.upvotes += 1
        else:
            comment.upvotes += 1
        
        comment.save()
        
        return JsonResponse({
            'success': True,
            'vote_count': comment.upvotes - comment.downvotes,
            'user_vote': 'upvote' if created else None
        })
    
    return JsonResponse({'success': False})


@login_required
def comment_downvote(request, pk):
    """Downvote comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=comment.pk,
            defaults={'vote_type': 'downvote'}
        )
        
        if not created:
            if vote.vote_type == 'downvote':
                vote.delete()
                comment.downvotes -= 1
            else:
                vote.vote_type = 'downvote'
                vote.save()
                comment.upvotes -= 1
                comment.downvotes += 1
        else:
            comment.downvotes += 1
        
        comment.save()
        
        return JsonResponse({
            'success': True,
            'vote_count': comment.upvotes - comment.downvotes,
            'user_vote': 'downvote' if created else None
        })
    
    return JsonResponse({'success': False})


# Bookmark views
@login_required
def discussion_bookmark(request, pk):
    """Bookmark/unbookmark discussion"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if request.method == 'POST':
        bookmark, created = DiscussionBookmark.objects.get_or_create(
            user=request.user,
            discussion=discussion
        )
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({
            'success': True,
            'bookmarked': bookmarked
        })
    
    return JsonResponse({'success': False})


@login_required
def bookmark_list(request):
    """List user's bookmarks"""
    bookmarks = DiscussionBookmark.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookmarks': bookmarks,
    }
    
    return render(request, 'discussions/bookmark_list.html', context)


def discussion_by_tag(request, tag):
    """List discussions by tag"""
    discussions = Discussion.objects.filter(tags__icontains=tag).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(discussions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
    }
    
    return render(request, 'discussions/discussion_list.html', context)
