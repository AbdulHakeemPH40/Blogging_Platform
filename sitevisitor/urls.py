from django.urls import path
from .views import home, registration, sign_in, forgot_password, resetting_password, error_page, verify_otp

urlpatterns = [
    path('', home, name='home'),
    path('sign_up/', registration, name='registration'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('sign_in/', sign_in, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('resetting_password/', resetting_password, name='resetting_password'),
    path('404/', error_page, name='error_page'),
]
