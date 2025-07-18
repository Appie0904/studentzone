from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:pk>/apply/', views.project_apply, name='project_apply'),
    path('<int:pk>/join/', views.project_join, name='project_join'),
    path('<int:pk>/leave/', views.project_leave, name='project_leave'),
    
    # Applications
    path('applications/', views.application_list, name='application_list'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/<int:pk>/accept/', views.application_accept, name='application_accept'),
    path('application/<int:pk>/reject/', views.application_reject, name='application_reject'),
    
    # Study Partners
    path('partners/', views.partner_list, name='partner_list'),
    path('partners/create/', views.partner_create, name='partner_create'),
    path('partners/<int:pk>/', views.partner_detail, name='partner_detail'),
    path('partners/<int:pk>/edit/', views.partner_edit, name='partner_edit'),
    path('partners/<int:pk>/request/', views.partner_request, name='partner_request'),
    
    # Partner Requests
    path('requests/', views.request_list, name='request_list'),
    path('request/<int:pk>/', views.request_detail, name='request_detail'),
    path('request/<int:pk>/accept/', views.request_accept, name='request_accept'),
    path('request/<int:pk>/reject/', views.request_reject, name='request_reject'),
] 