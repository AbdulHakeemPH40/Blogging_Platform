from django.urls import path
from .views import admin_login

urlpatterns = [
    path('', admin_login, name='admin_login'),
    
    
    # Admin user profile view
]
