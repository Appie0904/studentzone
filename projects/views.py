from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Project, ProjectMembership, ProjectApplication, StudyPartner, StudyPartnerRequest
from .forms import ProjectForm, StudyPartnerForm
from communities.models import Community
from core.models import StudyField, University
from django.utils import timezone


def project_list(request):
    """List all projects"""
    projects = Project.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    # Filter by type
    project_type = request.GET.get('type')
    if project_type:
        projects = projects.filter(project_type=project_type)
    
    # Search
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'selected_status': status,
        'selected_type': project_type,
        'search': search,
    }
    
    return render(request, 'projects/project_list.html', context)


@login_required
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            
            messages.success(request, 'Project created successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'title': 'Create Project'
    }
    
    return render(request, 'projects/project_form.html', context)


def project_detail(request, pk):
    """View project details"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is a member
    is_member = False
    user_role = None
    if request.user.is_authenticated:
        try:
            membership = project.memberships.get(user=request.user, is_active=True)
            is_member = True
            user_role = membership.role
        except ProjectMembership.DoesNotExist:
            pass
    
    # Check if user has applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = project.applications.filter(applicant=request.user).exists()
    
    context = {
        'project': project,
        'is_member': is_member,
        'user_role': user_role,
        'has_applied': has_applied,
    }
    
    return render(request, 'projects/project_detail.html', context)


@login_required
def project_edit(request, pk):
    """Edit project"""
    project = get_object_or_404(Project, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'title': 'Edit Project'
    }
    
    return render(request, 'projects/project_form.html', context)


@login_required
def project_delete(request, pk):
    """Delete project"""
    project = get_object_or_404(Project, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('projects:project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def project_apply(request, pk):
    """Apply to join a project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        motivation = request.POST.get('motivation')
        relevant_experience = request.POST.get('relevant_experience')
        time_commitment = request.POST.get('time_commitment')
        skills = request.POST.get('skills')
        
        if motivation and relevant_experience and time_commitment and skills:
            application = ProjectApplication.objects.create(
                project=project,
                applicant=request.user,
                motivation=motivation,
                relevant_experience=relevant_experience,
                time_commitment=time_commitment,
                skills=skills
            )
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('projects:project_detail', pk=project.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'projects/project_apply.html', {'project': project})


@login_required
def project_join(request, pk):
    """Join a project directly"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        membership, created = ProjectMembership.objects.get_or_create(
            user=request.user,
            project=project,
            defaults={'role': 'member'}
        )
        
        if created:
            messages.success(request, f'You have joined "{project.title}"!')
        else:
            membership.is_active = True
            membership.save()
            messages.success(request, f'You have rejoined "{project.title}"!')
    
    return redirect('projects:project_detail', pk=project.pk)


@login_required
def project_leave(request, pk):
    """Leave a project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        try:
            membership = project.memberships.get(user=request.user)
            membership.is_active = False
            membership.save()
            messages.success(request, f'You have left "{project.title}".')
        except ProjectMembership.DoesNotExist:
            messages.error(request, 'You are not a member of this project.')
    
    return redirect('projects:project_detail', pk=project.pk)


# Application views
@login_required
def application_list(request):
    """List applications for user's projects"""
    applications = ProjectApplication.objects.filter(
        project__creator=request.user
    ).order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    
    return render(request, 'projects/application_list.html', context)


@login_required
def application_detail(request, pk):
    """View application details"""
    application = get_object_or_404(ProjectApplication, pk=pk)
    
    # Check if user is the project creator
    if application.project.creator != request.user:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('projects:project_list')
    
    context = {
        'application': application,
    }
    
    return render(request, 'projects/application_detail.html', context)


@login_required
def application_accept(request, pk):
    """Accept application"""
    application = get_object_or_404(ProjectApplication, pk=pk)
    
    # Check if user is the project creator
    if application.project.creator != request.user:
        messages.error(request, 'You do not have permission to accept this application.')
        return redirect('projects:application_list')
    
    if request.method == 'POST':
        application.status = 'accepted'
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()
        
        # Add user to project
        ProjectMembership.objects.create(
            user=application.applicant,
            project=application.project,
            role='member'
        )
        
        messages.success(request, f'Application from {application.applicant.username} accepted!')
    
    return redirect('projects:application_detail', pk=application.pk)


@login_required
def application_reject(request, pk):
    """Reject application"""
    application = get_object_or_404(ProjectApplication, pk=pk)
    
    # Check if user is the project creator
    if application.project.creator != request.user:
        messages.error(request, 'You do not have permission to reject this application.')
        return redirect('projects:application_list')
    
    if request.method == 'POST':
        application.status = 'rejected'
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()
        
        messages.success(request, f'Application from {application.applicant.username} rejected.')
    
    return redirect('projects:application_detail', pk=application.pk)


# Study Partner views
def partner_list(request):
    """List study partners"""
    partners = StudyPartner.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by study field
    study_field = request.GET.get('study_field')
    if study_field:
        partners = partners.filter(study_field_id=study_field)
    
    # Filter by university
    university = request.GET.get('university')
    if university:
        partners = partners.filter(university_id=university)
    
    # Pagination
    paginator = Paginator(partners, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    study_fields = StudyField.objects.filter(is_active=True).order_by('name')
    universities = University.objects.all().order_by('name')
    
    context = {
        'page_obj': page_obj,
        'study_fields': study_fields,
        'universities': universities,
        'selected_field': study_field,
        'selected_university': university,
    }
    
    return render(request, 'projects/partner_list.html', context)


@login_required
def partner_create(request):
    """Create study partner profile"""
    if request.method == 'POST':
        study_field_id = request.POST.get('study_field')
        university_id = request.POST.get('university')
        preferred_study_methods = request.POST.get('preferred_study_methods', '')
        subjects_of_interest = request.POST.get('subjects_of_interest', '')
        availability = request.POST.get('availability', '')
        
        if study_field_id and university_id:
            partner, created = StudyPartner.objects.get_or_create(
                user=request.user,
                study_field_id=study_field_id,
                university_id=university_id,
                defaults={
                    'preferred_study_methods': preferred_study_methods,
                    'subjects_of_interest': subjects_of_interest,
                    'availability': availability,
                }
            )
            
            if not created:
                partner.preferred_study_methods = preferred_study_methods
                partner.subjects_of_interest = subjects_of_interest
                partner.availability = availability
                partner.save()
            
            messages.success(request, 'Study partner profile updated successfully!')
            return redirect('projects:partner_detail', pk=partner.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    study_fields = StudyField.objects.filter(is_active=True).order_by('name')
    universities = University.objects.all().order_by('name')
    
    context = {
        'study_fields': study_fields,
        'universities': universities,
    }
    
    return render(request, 'projects/partner_form.html', context)


def partner_detail(request, pk):
    """View study partner profile"""
    partner = get_object_or_404(StudyPartner, pk=pk, is_active=True)
    
    context = {
        'partner': partner,
    }
    
    return render(request, 'projects/partner_detail.html', context)


@login_required
def partner_edit(request, pk):
    """Edit study partner profile"""
    partner = get_object_or_404(StudyPartner, pk=pk, user=request.user)
    
    if request.method == 'POST':
        partner.preferred_study_methods = request.POST.get('preferred_study_methods', '')
        partner.subjects_of_interest = request.POST.get('subjects_of_interest', '')
        partner.availability = request.POST.get('availability', '')
        partner.save()
        
        messages.success(request, 'Study partner profile updated successfully!')
        return redirect('projects:partner_detail', pk=partner.pk)
    
    study_fields = StudyField.objects.filter(is_active=True).order_by('name')
    universities = University.objects.all().order_by('name')
    
    context = {
        'partner': partner,
        'study_fields': study_fields,
        'universities': universities,
    }
    
    return render(request, 'projects/partner_form.html', context)


@login_required
def partner_request(request, pk):
    """Send study partner request"""
    partner = get_object_or_404(StudyPartner, pk=pk, is_active=True)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        proposed_meeting_time = request.POST.get('proposed_meeting_time')
        meeting_location = request.POST.get('meeting_location', '')
        
        if message:
            request_obj = StudyPartnerRequest.objects.create(
                requester=request.user,
                recipient=partner.user,
                study_field=partner.study_field,
                message=message,
                proposed_meeting_time=proposed_meeting_time,
                meeting_location=meeting_location,
            )
            
            messages.success(request, f'Study partner request sent to {partner.user.username}!')
            return redirect('projects:partner_detail', pk=partner.pk)
        else:
            messages.error(request, 'Please enter a message.')
    
    return render(request, 'projects/partner_request.html', {'partner': partner})


# Request views
@login_required
def request_list(request):
    """List study partner requests"""
    received_requests = StudyPartnerRequest.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    sent_requests = StudyPartnerRequest.objects.filter(
        requester=request.user
    ).order_by('-created_at')
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'projects/request_list.html', context)


def request_detail(request, pk):
    """View study partner request"""
    request_obj = get_object_or_404(StudyPartnerRequest, pk=pk)
    
    # Check if user is involved in the request
    if request.user not in [request_obj.requester, request_obj.recipient]:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('projects:request_list')
    
    context = {
        'request_obj': request_obj,
    }
    
    return render(request, 'projects/request_detail.html', context)


@login_required
def request_accept(request, pk):
    """Accept study partner request"""
    request_obj = get_object_or_404(StudyPartnerRequest, pk=pk, recipient=request.user)
    
    if request.method == 'POST':
        request_obj.status = 'accepted'
        request_obj.responded_at = timezone.now()
        request_obj.save()
        
        messages.success(request, f'Study partner request from {request_obj.requester.username} accepted!')
    
    return redirect('projects:request_detail', pk=request_obj.pk)


@login_required
def request_reject(request, pk):
    """Reject study partner request"""
    request_obj = get_object_or_404(StudyPartnerRequest, pk=pk, recipient=request.user)
    
    if request.method == 'POST':
        request_obj.status = 'rejected'
        request_obj.responded_at = timezone.now()
        request_obj.save()
        
        messages.success(request, f'Study partner request from {request_obj.requester.username} rejected.')
    
    return redirect('projects:request_detail', pk=request_obj.pk)
