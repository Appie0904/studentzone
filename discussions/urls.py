from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('create/', views.discussion_create, name='discussion_create'),
    path('<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('<int:pk>/edit/', views.discussion_edit, name='discussion_edit'),
    path('<int:pk>/delete/', views.discussion_delete, name='discussion_delete'),
    path('<int:pk>/pin/', views.discussion_pin, name='discussion_pin'),
    path('<int:pk>/close/', views.discussion_close, name='discussion_close'),
    
    # Comments
    path('<int:discussion_pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:pk>/solution/', views.comment_solution, name='comment_solution'),
    
    # Voting
    path('<int:pk>/upvote/', views.discussion_upvote, name='discussion_upvote'),
    path('<int:pk>/downvote/', views.discussion_downvote, name='discussion_downvote'),
    path('comment/<int:pk>/upvote/', views.comment_upvote, name='comment_upvote'),
    path('comment/<int:pk>/downvote/', views.comment_downvote, name='comment_downvote'),
    
    # Bookmarks
    path('<int:pk>/bookmark/', views.discussion_bookmark, name='discussion_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    
    # Tags
    path('tag/<str:tag>/', views.discussion_by_tag, name='discussion_by_tag'),
] 