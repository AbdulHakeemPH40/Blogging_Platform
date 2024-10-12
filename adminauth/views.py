from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AdminLoginForm



def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_staff:  # Corrected 'none' to 'None'
                auth_login(request, user)
                return redirect('admin_home')  # Redirect to admin home if login is successful
            else:
                messages.error(request, "You do not have permission to access the admin panel.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AdminLoginForm()
    
    return render(request, 'adminauth/admin_login.html', {'form': form})


