from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('upload/', views.resource_upload, name='resource_upload'),
    path('<int:pk>/', views.resource_detail, name='resource_detail'),
    path('<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('<int:pk>/delete/', views.resource_delete, name='resource_delete'),
    path('<int:pk>/download/', views.resource_download, name='resource_download'),
    
    # Voting
    path('<int:pk>/vote/', views.resource_vote, name='resource_vote'),
    
    # Comments
    path('<int:pk>/comment/', views.resource_comment_create, name='resource_comment_create'),
    path('<int:pk>/comment/<int:comment_pk>/edit/', views.resource_comment_edit, name='resource_comment_edit'),
    path('<int:pk>/comment/<int:comment_pk>/delete/', views.resource_comment_delete, name='resource_comment_delete'),
    
    # Bookmarks
    path('<int:pk>/bookmark/', views.resource_bookmark, name='resource_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    
    # Collections
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/create/', views.collection_create, name='collection_create'),
    path('collections/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('collections/<int:pk>/edit/', views.collection_edit, name='collection_edit'),
    path('collections/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    
    # Categories
    path('category/<slug:category_slug>/', views.resource_by_category, name='resource_by_category'),
    
    # Study Fields
    path('field/<slug:field_slug>/', views.resource_by_field, name='resource_by_field'),
    
    # Reports
    path('<int:pk>/report/', views.resource_report, name='resource_report'),
] 