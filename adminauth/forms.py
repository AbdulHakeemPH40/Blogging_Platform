from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )
