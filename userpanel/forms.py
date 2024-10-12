from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User_Table, Blog, Comment,GENDER_CHOICES

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password", 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your blog title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write your blog content here.'}),
            'blog_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'status': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        # widgets = {
        #     'comment': forms.Textarea(attrs={'class': 'form-control'})
        # }

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    class Meta:
        model = User_Table
        fields = ['phone', 'profile_image', 'cover_photo', 'id_proof', 'profile_description']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cover_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'profile_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about yourself...'})
        }

    def save(self, commit=True):
        # Save the User model fields (first_name, last_name, username, email)
        user = self.instance.user  # Assuming the instance is linked to a User_Table object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Save the User model fields

        # Save the User_Table fields
        profile = super(UserProfileForm, self).save(commit=False)
        if commit:
            profile.save()  # Save the User_Table model fields

        return profile


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your old password'
        })
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        })
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
