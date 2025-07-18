from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Community, CommunityMembership, CommunityEvent, EventParticipant
from .forms import CommunityForm, CommunityEventForm
from core.models import StudyField
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CommunityInvitation


User = get_user_model()


def community_list(request):
    """List all communities"""
    communities = Community.objects.filter(is_active=True).order_by('-member_count')
    
    # Filter by study field
    study_field = request.GET.get('study_field')
    if study_field:
        communities = communities.filter(study_field_id=study_field)
    
    # Search
    search = request.GET.get('search')
    if search:
        communities = communities.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(communities, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    study_fields = StudyField.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'study_fields': study_fields,
        'selected_field': study_field,
        'search': search,
    }
    
    return render(request, 'communities/community_list.html', context)


@login_required
def community_create(request):
    """Create a new community"""
    if request.method == 'POST':
        print(f"DEBUG: Form submitted with data: {request.POST}")
        form = CommunityForm(request.POST)
        print(f"DEBUG: Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            print(f"DEBUG: Form is valid, creating community...")
            try:
                community = form.save(commit=False)
                community.created_by = request.user
                community.save()
                
                # Auto-join the creator
                CommunityMembership.objects.create(
                    user=request.user,
                    community=community,
                    role='admin'
                )
                
                messages.success(request, f'Community "{community.name}" created successfully!')
                return redirect('communities:community_detail', pk=community.pk)
            except Exception as e:
                print(f"DEBUG: Error creating community: {e}")
                messages.error(request, f'Error creating community: {str(e)}')
        else:
            print(f"DEBUG: Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CommunityForm()
    
    context = {
        'form': form,
        'title': 'Create Community'
    }
    
    return render(request, 'communities/community_form.html', context)


def community_detail(request, pk):
    """View community details"""
    community = get_object_or_404(Community, pk=pk, is_active=True)
    
    # Check if user is a member
    is_member = False
    user_role = None
    if request.user.is_authenticated:
        try:
            membership = community.memberships.get(user=request.user, is_active=True)
            is_member = True
            user_role = membership.role
        except CommunityMembership.DoesNotExist:
            pass
    
    # Get recent discussions
    recent_discussions = community.discussions.order_by('-created_at')[:5]
    
    # Get upcoming events
    upcoming_events = community.events.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time')[:3]
    
    # Get recent resources
    recent_resources = community.resources.filter(
        is_approved=True,
        is_public=True
    ).order_by('-created_at')[:5]
    
    context = {
        'community': community,
        'is_member': is_member,
        'user_role': user_role,
        'recent_discussions': recent_discussions,
        'upcoming_events': upcoming_events,
        'recent_resources': recent_resources,
    }
    
    return render(request, 'communities/community_detail.html', context)


@login_required
def community_edit(request, pk):
    """Edit community"""
    community = get_object_or_404(Community, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, 'Community updated successfully!')
            return redirect('communities:community_detail', pk=community.pk)
    else:
        form = CommunityForm(instance=community)
    
    context = {
        'form': form,
        'community': community,
        'title': 'Edit Community'
    }
    
    return render(request, 'communities/community_form.html', context)


@login_required
def community_join(request, pk):
    """Join a community"""
    community = get_object_or_404(Community, pk=pk, is_active=True)
    
    if request.method == 'POST':
        membership, created = CommunityMembership.objects.get_or_create(
            user=request.user,
            community=community,
            defaults={'role': 'member'}
        )
        
        if created:
            messages.success(request, f'You have joined "{community.name}"!')
        else:
            membership.is_active = True
            membership.save()
            messages.success(request, f'You have rejoined "{community.name}"!')
    
    return redirect('communities:community_detail', pk=community.pk)


@login_required
def community_leave(request, pk):
    """Leave a community"""
    community = get_object_or_404(Community, pk=pk, is_active=True)
    
    if request.method == 'POST':
        try:
            membership = community.memberships.get(user=request.user)
            membership.is_active = False
            membership.save()
            messages.success(request, f'You have left "{community.name}".')
        except CommunityMembership.DoesNotExist:
            messages.error(request, 'You are not a member of this community.')
    
    return redirect('communities:community_detail', pk=community.pk)


@login_required
def community_invite(request, pk):
    """Invite users to community"""
    community = get_object_or_404(Community, pk=pk, is_active=True)
    
    # Check if user has permission to invite
    try:
        membership = community.memberships.get(user=request.user, is_active=True)
        if membership.role not in ['admin', 'moderator']:
            messages.error(request, 'You do not have permission to invite users.')
            return redirect('communities:community_detail', pk=community.pk)
    except CommunityMembership.DoesNotExist:
        messages.error(request, 'You are not a member of this community.')
        return redirect('communities:community_detail', pk=community.pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        message = request.POST.get('message', '')
        
        try:
            invited_user = User.objects.get(username=username)
            
            # Check if already invited
            if community.invitations.filter(invited_user=invited_user, status='pending').exists():
                messages.error(request, f'{username} has already been invited.')
            else:
                # Create invitation
                CommunityInvitation.objects.create(
                    community=community,
                    invited_by=request.user,
                    invited_user=invited_user,
                    message=message,
                    expires_at=timezone.now() + timedelta(days=7)
                )
                messages.success(request, f'Invitation sent to {username}!')
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
    
    return redirect('communities:community_detail', pk=community.pk)


# Event views
def event_list(request, community_pk):
    """List events for a community"""
    community = get_object_or_404(Community, pk=community_pk, is_active=True)
    events = community.events.order_by('start_time')
    
    context = {
        'community': community,
        'events': events,
    }
    
    return render(request, 'communities/event_list.html', context)


@login_required
def event_create(request, community_pk):
    """Create a new event"""
    community = get_object_or_404(Community, pk=community_pk, is_active=True)
    
    # Check if user has permission
    try:
        membership = community.memberships.get(user=request.user, is_active=True)
        if membership.role not in ['admin', 'moderator']:
            messages.error(request, 'You do not have permission to create events.')
            return redirect('communities:community_detail', pk=community.pk)
    except CommunityMembership.DoesNotExist:
        messages.error(request, 'You are not a member of this community.')
        return redirect('communities:community_detail', pk=community.pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '')
        online_link = request.POST.get('online_link', '')
        
        if title and description and event_type and start_time and end_time:
            event = CommunityEvent.objects.create(
                community=community,
                title=title,
                description=description,
                event_type=event_type,
                start_time=start_time,
                end_time=end_time,
                location=location,
                online_link=online_link,
                created_by=request.user
            )
            
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('communities:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'community': community,
    }
    
    return render(request, 'communities/event_form.html', context)


def event_detail(request, pk):
    """View event details"""
    event = get_object_or_404(CommunityEvent, pk=pk)
    
    # Check if user is registered
    is_registered = False
    if request.user.is_authenticated:
        is_registered = event.participants.filter(user=request.user).exists()
    
    context = {
        'event': event,
        'is_registered': is_registered,
    }
    
    return render(request, 'communities/event_detail.html', context)


@login_required
def event_edit(request, pk):
    """Edit event"""
    event = get_object_or_404(CommunityEvent, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.event_type = request.POST.get('event_type')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.location = request.POST.get('location', '')
        event.online_link = request.POST.get('online_link', '')
        event.save()
        
        messages.success(request, 'Event updated successfully!')
        return redirect('communities:event_detail', pk=event.pk)
    
    context = {
        'event': event,
    }
    
    return render(request, 'communities/event_form.html', context)


@login_required
def event_register(request, pk):
    """Register for an event"""
    event = get_object_or_404(CommunityEvent, pk=pk)
    
    if request.method == 'POST':
        participant, created = EventParticipant.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'status': 'registered'}
        )
        
        if created:
            messages.success(request, f'You have registered for "{event.title}"!')
        else:
            messages.info(request, 'You are already registered for this event.')
    
    return redirect('communities:event_detail', pk=event.pk)


@login_required
def event_unregister(request, pk):
    """Unregister from an event"""
    event = get_object_or_404(CommunityEvent, pk=pk)
    
    if request.method == 'POST':
        try:
            participant = event.participants.get(user=request.user)
            participant.delete()
            messages.success(request, f'You have unregistered from "{event.title}".')
        except EventParticipant.DoesNotExist:
            messages.error(request, 'You are not registered for this event.')
    
    return redirect('communities:event_detail', pk=event.pk)
