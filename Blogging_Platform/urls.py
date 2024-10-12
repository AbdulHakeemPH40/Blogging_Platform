"""
URL configuration for Blogging_Platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# urls.py in Blogging_Platform

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('adminauth/', include('adminauth.urls')),  # Admin authentication URLs
    path('adminpanel/', include('adminpanel.urls')),  # Admin panel URLs
    path('user/', include('userpanel.urls')),  # User panel URLs
    path('', include('sitevisitor.urls')),  # Site visitor URLs
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
