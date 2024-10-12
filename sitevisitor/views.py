from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from userpanel.models import Blog, User_Table
from .forms import RegistrationForm
from userpanel.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def registration(request):
    """Handle the user registration process."""
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, request.FILES)  # Include request.FILES for file handling

        if registration_form.is_valid():
            # Save the User model data
            new_user = registration_form.save()

            # Check if User_Table already exists
            user_table_exists = User_Table.objects.filter(user=new_user).exists()

            if not user_table_exists:
                # Now create a User_Table entry
                user_profile = User_Table.objects.create(
                    user=new_user,
                    phone=registration_form.cleaned_data.get('phone'),
                    gender=registration_form.cleaned_data.get('gender'),
                    profile_description=registration_form.cleaned_data.get('profile_description'),
                    profile_image=registration_form.cleaned_data.get('profile_image'),
                    id_proof=registration_form.cleaned_data.get('id_proof')
                )

            # Log in the new user
            auth_login(request, new_user)
            messages.success(request, "Registration successful. Enjoy With Your Blog.")
            return redirect('user_home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        registration_form = RegistrationForm()

    context = {'form': registration_form}
    return render(request, 'sitevisitor/registration.html', context)

def sign_in(request):
    """Handle the sign-in process for site visitors."""
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user has a profile in User_Table
                try:
                    user_profile = User_Table.objects.get(user=user)
                except User_Table.DoesNotExist:
                    # Auto-create a profile for the user
                    user_profile = User_Table.objects.create(user=user)
                    messages.info(request, "User profile created successfully.")

                # Now check if the user is blocked
                if user_profile.is_blocked:
                    messages.error(request, "Your account is blocked. Please contact the administrator.")
                    return redirect('sign_in')

                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('user_home')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        login_form = LoginForm()

    context = {'form': login_form}
    return render(request, 'sitevisitor/login.html', context)


def home(request):
    """Render the home page with a list of published blogs."""
    published_blogs = Blog.objects.filter(status='published').order_by('-created_at')
    context = {'blogs': published_blogs}
    return render(request, 'sitevisitor/home.html', context)

def forgot_password(request):
    """Handle password reset."""
    if request.method == 'POST':
        user_email = request.POST.get('email')
        users = User.objects.filter(email=user_email)
        
        if users.exists():
            for user in users:
                # Store the user ID in session for each user (if needed) and send reset email
                send_reset_email(user)
            messages.success(request, "Password reset email has been sent.")
            return redirect('login')
        else:
            messages.error(request, "No user found with this email address.")
    
    return render(request, 'sitevisitor/forgot_password.html')

def send_reset_email(user):
    # Logic to send reset email to the user
    pass


def resetting_password(request):
    """Allow the user to reset their password."""
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()

            messages.success(request, 'Password reset successfully. You can now log in with your new password.')
            return redirect('login')  # Redirect to login page
        else:
            # Add the error message for password mismatch
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'sitevisitor/reset_password.html')


def error_page(request):
    """Render the custom 404 error page."""
    return render(request, 'sitevisitor/404.html')

def verify_otp(request):
    return render(request, 'sitevisitor/verify_otp.html')
