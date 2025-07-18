from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('create/', views.community_create, name='community_create'),
    path('<int:pk>/', views.community_detail, name='community_detail'),
    path('<int:pk>/edit/', views.community_edit, name='community_edit'),
    path('<int:pk>/join/', views.community_join, name='community_join'),
    path('<int:pk>/leave/', views.community_leave, name='community_leave'),
    path('<int:pk>/invite/', views.community_invite, name='community_invite'),
    
    # Events
    path('<int:community_pk>/events/', views.event_list, name='event_list'),
    path('<int:community_pk>/events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    path('events/<int:pk>/unregister/', views.event_unregister, name='event_unregister'),
] 