from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from userpanel.models import Blog, User_Table, Comment
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages


@login_required(login_url='/404/')
def admin_home(request):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    # Add welcome message only once after login
    if 'welcome_message_displayed' not in request.session:
        messages.success(request, f"Welcome back, {request.user.first_name}!")
        request.session['welcome_message_displayed'] = True  # Set the flag so the message doesn't reappear

    # Fetch counts for users, blogs, and comments.
    users_count = User_Table.objects.count()
    blogs_count = Blog.objects.count()
    comments_count = Comment.objects.count()

    # Prepare the context with recent blogs and comments.
    context = {
        'users_count': users_count,
        'blogs_count': blogs_count,
        'comments_count': comments_count,
        'recent_blogs': Blog.objects.order_by('-created_at')[:10],
        'recent_comments': Comment.objects.order_by('-created_at')[:10],
    }

    return render(request, 'adminpanel/admin_home.html', context)


@login_required(login_url='/404/')
def block_user(request, user_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    user_profile = get_object_or_404(User_Table, id=user_id)
    user_profile.is_blocked = True
    user_profile.save()
    user_profile.user.is_active = False  # Deactivate the user account.
    user_profile.user.save()

    # Hide all blogs of the blocked user.
    Blog.objects.filter(author=user_profile.user).update(status='hidden')

    # Hide all comments of the blocked user.
    Comment.objects.filter(author=user_profile.user).update(status='hidden')

    messages.success(request, f'User {user_profile.user.username} has been blocked successfully.')
    return redirect('user_list')


# Admin-specific view to unblock a user.
@login_required(login_url='/404/')
def unblock_user(request, user_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    user_profile = get_object_or_404(User_Table, id=user_id)
    user_profile.is_blocked = False
    user_profile.save()
    user_profile.user.is_active = True  # Reactivate the user account.
    user_profile.user.save()

    # Set all blogs to draft for review.
    Blog.objects.filter(author=user_profile.user).update(status='draft')

    # Optionally, set comments to visible or keep them hidden until reviewed.
    Comment.objects.filter(author=user_profile.user).update(status='hidden')  # Adjust as needed

    messages.success(request, f'User {user_profile.user.username} has been unblocked successfully.')
    return redirect('user_list')


# Admin Home View (Dashboard)
# Requires the user to be logged in and a staff member.


# View for listing all users.
# Requires the user to be logged in and a staff member.
@login_required(login_url='/404/')
def user_list(request):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    users = User_Table.objects.all()
    return render(request, 'adminpanel/user_list.html', {'users': users})


# View for viewing details of a single user.
# Requires the user to be logged in and a staff member.
@login_required(login_url='/404/')
def view_user(request, user_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    user = get_object_or_404(User_Table, id=user_id)
    blogs = Blog.objects.filter(author=user.user, status='published').order_by('-created_at')

    return render(request, 'adminpanel/view_user.html', {
        'user_profile': user,
    })


# View for listing all blogs.
# Requires the user to be logged in and a staff member.
@login_required(login_url='/404/')
def blog_list(request):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    section = request.GET.get('section', 'published')  # Get the blog section (published,).

    if section == 'published':
        blogs = Blog.objects.filter(status='published').order_by('-created_at')
    elif section == 'hidden':
        blogs = Blog.objects.filter(status='hidden').order_by('-updated_at')

    return render(request, 'adminpanel/blog_list.html', {
        'section': section,
        'published_blogs': blogs if section == 'published' else None,
        'hidden_blogs': blogs if section == 'hidden' else None,
    })


# View for resetting the admin's password.
# Requires the user to be logged in and a staff member.
@login_required(login_url='/404/')
def reset_password(request):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after the password change.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'adminpanel/reset_password.html', {'form': form})


# Admin-specific view for viewing blog details along with comments.
# Requires the user to be a staff member.
@login_required(login_url='/404/')
def admin_view_blog(request, blog_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    bLog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=bLog)
    return render(request, 'adminpanel/admin_view_blog.html', {'Blog': bLog, 'comments': comments})


# Admin view to hide a blog.
# Requires the user to be a staff member.
@login_required(login_url='/404/')
def admin_hide_blog(request, blog_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    blog = get_object_or_404(Blog, id=blog_id)
    blog.status = 'hidden'
    blog.save()
    messages.success(request, 'Blog has been hidden successfully.')
    return redirect('admin_view_blog', blog_id=blog_id)


# Admin view to show a hidden blog.
# Requires the user to be a staff member.
@login_required(login_url='/404/')
def admin_show_blog(request, blog_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the author of the blog is blocked
    if blog.author.user_table.is_blocked:
        messages.error(request, 'This user is blocked. Unblock the user before making their blog visible.')
        return redirect('admin_view_blog', blog_id=blog_id)

    blog.status = 'published'
    blog.save()
    messages.success(request, 'Blog has been made visible successfully.')
    return redirect('admin_view_blog', blog_id=blog_id)


# Admin view to hide a comment.
# Requires the user to be a staff member.
@login_required(login_url='/404/')
def admin_hide_comment(request, comment_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'hidden'
    comment.save()
    messages.success(request, 'Comment has been hidden successfully.')
    return redirect('admin_view_blog', blog_id=comment.blog.id)


# Admin view to show a hidden comment.
# Requires the user to be a staff member.
@login_required(login_url='/404/')
def admin_show_comment(request, comment_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the author of the comment is blocked
    if comment.author.user_table.is_blocked:
        messages.error(request, 'This user is blocked. Unblock the user before making their comment visible.')
        return redirect('admin_view_blog', blog_id=comment.blog.id)

    comment.status = 'visible'
    comment.save()
    messages.success(request, 'Comment has been made visible successfully.')
    return redirect('admin_view_blog', blog_id=comment.blog.id)


# Admin-specific view for viewing a user's profile with their blogs and comments.
@login_required(login_url='/admin_login/')
def admin_view_user_profile(request, user_id):
    if not request.user.is_staff:
        return redirect('/admin_login/')  # Redirect to the login page if not a staff member.

    user_profile = get_object_or_404(User_Table, id=user_id)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'adminpanel/view_user_profile.html', context)


# Admin sign-out view
@login_required(login_url='/404/')
def admin_sign_out(request):
    logout(request)
    return redirect('admin_login')  # Redirect to the admin login page after logout
