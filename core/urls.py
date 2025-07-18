from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test-dropdown/', views.test_dropdown, name='test_dropdown'),
    path('logout/', views.logout_view, name='logout'),
    path('saml/metadata/', views.saml_metadata, name='saml_metadata'),
    path('saml/test/', views.saml_test, name='saml_test'),
    path('saml/test-login/', views.test_saml_login, name='test_saml_login'),
    path('dev/login/', views.dev_login, name='dev_login'),
] 