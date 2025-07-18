from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import UserProfile, University, StudyField
from .forms import UserProfileForm
from communities.models import Community
from discussions.models import Discussion
from projects.models import Project
from resources.models import Resource
from django.contrib.auth import logout


def home(request):
    """Home page with overview of platform activity"""
    context = {
        'total_users': User.objects.count(),
        'total_communities': Community.objects.filter(is_active=True).count(),
        'total_discussions': Discussion.objects.count(),
        'total_projects': Project.objects.filter(status='recruiting').count(),
        'total_resources': Resource.objects.filter(is_approved=True).count(),
    }
    
    if request.user.is_authenticated:
        # Get user's communities
        user_communities = Community.objects.filter(
            memberships__user=request.user,
            memberships__is_active=True
        )[:5]
        
        # Get recent discussions from user's communities
        recent_discussions = Discussion.objects.filter(
            community__in=user_communities
        ).order_by('-created_at')[:10]
        
        # Get featured projects
        featured_projects = Project.objects.filter(
            is_featured=True,
            status='recruiting'
        ).order_by('-created_at')[:5]
        
        # Get recent resources
        recent_resources = Resource.objects.filter(
            is_approved=True,
            is_public=True
        ).order_by('-created_at')[:5]
        
        context.update({
            'user_communities': user_communities,
            'recent_discussions': recent_discussions,
            'featured_projects': featured_projects,
            'recent_resources': recent_resources,
        })
    else:
        # Show public communities and discussions for non-authenticated users
        popular_communities = Community.objects.filter(
            is_active=True,
            is_public=True
        ).order_by('-member_count')[:5]
        
        recent_discussions = Discussion.objects.filter(
            community__is_public=True
        ).order_by('-created_at')[:10]
        
        context.update({
            'popular_communities': popular_communities,
            'recent_discussions': recent_discussions,
        })
    
    return render(request, 'core/home.html', context)


@login_required
def profile(request):
    """User's own profile page"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get user's activity
    user_discussions = Discussion.objects.filter(author=request.user).order_by('-created_at')[:5]
    user_resources = Resource.objects.filter(author=request.user).order_by('-created_at')[:5]
    user_projects = Project.objects.filter(creator=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'user_discussions': user_discussions,
        'user_resources': user_resources,
        'user_projects': user_projects,
    }
    
    return render(request, 'core/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'core/edit_profile.html', context)


def user_profile(request, username):
    """View another user's profile"""
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    # Get user's public activity
    user_discussions = Discussion.objects.filter(
        author=user,
        is_anonymous=False
    ).order_by('-created_at')[:5]
    
    user_resources = Resource.objects.filter(
        author=user,
        is_public=True,
        is_approved=True
    ).order_by('-created_at')[:5]
    
    context = {
        'viewed_user': user,
        'profile': profile,
        'user_discussions': user_discussions,
        'user_resources': user_resources,
    }
    
    return render(request, 'core/user_profile.html', context)


def search(request):
    """Search across all content"""
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Search discussions
        discussions = Discussion.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        ).order_by('-created_at')
        
        # Search resources
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query),
            is_approved=True,
            is_public=True
        ).order_by('-created_at')
        
        # Search projects
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')
        
        # Search communities
        communities = Community.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        ).order_by('name')
        
        # Search users
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).order_by('username')
        
        results = {
            'discussions': discussions,
            'resources': resources,
            'projects': projects,
            'communities': communities,
            'users': users,
        }
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'core/search.html', context)


def about(request):
    """About page"""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page"""
    return render(request, 'core/contact.html')


def test_dropdown(request):
    """Test dropdown functionality"""
    return render(request, 'core/test_dropdown.html')


def logout_view(request):
    """Log out the user and redirect to home"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('core:home')


def saml_metadata(request):
    """SAML metadata for SurfConext integration"""
    from djangosaml2.views import metadata
    return metadata(request)


def saml_test(request):
    """Test page for SAML configuration"""
    return render(request, 'core/saml_test.html')


def test_saml_login(request):
    """Test SAML login for development - simulates successful authentication"""
    from django.contrib.auth import get_user_model
    from django.contrib.auth import login
    
    User = get_user_model()
    
    # Create a test user if it doesn't exist
    test_user, created = User.objects.get_or_create(
        username='test.student',
        defaults={
            'email': 'test.student@tudelft.nl',
            'first_name': 'Test',
            'last_name': 'Student',
        }
    )
    
    if created:
        # Create user profile
        from .models import UserProfile, University
        university, _ = University.objects.get_or_create(
            code='tudelft.nl',
            defaults={
                'name': 'TU Delft',
                'abbreviation': 'TUD',
                'city': 'Delft',
                'is_active': True,
            }
        )
        
        profile = UserProfile.objects.create(
            user=test_user,
            university=university,
            study_level='bachelor',
            student_id='12345678',
            is_verified=True,
        )
    
    # Log in the user
    login(request, test_user)
    
    # Add success message
    from django.contrib import messages
    messages.success(request, f"Welcome {test_user.get_full_name()}! You have been logged in via SAML.")
    
    return redirect('core:home')


def dev_login(request):
    """Development login view that bypasses SAML for testing"""
    if request.method == 'POST':
        # Get form data
        university_code = request.POST.get('university', 'tudelft.nl')
        student_name = request.POST.get('student_name', 'Test Student')
        email = request.POST.get('email', 'test.student@tudelft.nl')
        student_id = request.POST.get('student_id', '12345678')
        
        # Parse student name
        name_parts = student_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else 'Test'
        last_name = name_parts[1] if len(name_parts) > 1 else 'Student'
        
        # Generate username from email
        username = email.split('@')[0]
        
        from django.contrib.auth import get_user_model
        from django.contrib.auth import login
        
        User = get_user_model()
        
        # Create or get user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        
        if created:
            # Create user profile
            from .models import UserProfile, University
            university, _ = University.objects.get_or_create(
                code=university_code,
                defaults={
                    'name': university_code.replace('.nl', '').upper(),
                    'abbreviation': university_code.split('.')[0].upper(),
                    'city': 'Unknown',
                    'is_active': True,
                }
            )
            
            profile = UserProfile.objects.create(
                user=user,
                university=university,
                study_level='bachelor',
                student_id=student_id,
                is_verified=True,
            )
        else:
            # Update existing user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Update profile
            try:
                profile = user.profile
                profile.student_id = student_id
                profile.save()
            except UserProfile.DoesNotExist:
                pass
        
        # Log in the user
        login(request, user)
        
        # Add success message
        from django.contrib import messages
        messages.success(request, f"Welcome {user.get_full_name()}! You have been logged in via development SAML simulation.")
        
        return redirect('core:home')
    
    return render(request, 'core/dev_login.html')
