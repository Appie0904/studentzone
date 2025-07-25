"""
URL configuration for studentzone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # SAML Authentication URLs
    path('saml2/', include('djangosaml2.urls')),
    
    # Legacy Authentication URLs (for fallback)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout handled by core app
    # Note: register and settings views need to be implemented properly
    # For now, redirecting to home page
    path('register/', auth_views.LoginView.as_view(template_name='registration/register.html'), name='register'),
    path('settings/', auth_views.LoginView.as_view(template_name='registration/settings.html'), name='settings'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # App URLs
    path('', include('core.urls')),
    path('communities/', include('communities.urls')),
    path('discussions/', include('discussions.urls')),
    path('projects/', include('projects.urls')),
    path('resources/', include('resources.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
