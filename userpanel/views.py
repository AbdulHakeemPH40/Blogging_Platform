from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .forms import BlogForm, CommentForm, UserProfileForm, CustomPasswordChangeForm
from .models import Blog, Comment, User_Table

@login_required(login_url='/404/')
def user_home(request):
    # Display all published blogs authored by non-blocked users
    blogs = Blog.objects.filter(status='published', author__user_table__is_blocked=False).order_by('-created_at')
    return render(request, 'userpanel/user_home.html', {'bLogs': blogs})

@login_required(login_url='/404/')
def user_blog_list(request):
    blogs = Blog.objects.filter(status='published', author__user_table__is_blocked=False).order_by('-created_at')
    return render(request, 'userpanel/blog_list.html', {'bLogs': blogs})


@login_required(login_url='/404/')
def view_blog(request, blog_id):
    # View a specific published blog and its visible comments
    blog = get_object_or_404(Blog, id=blog_id, status='published', author__user_table__is_blocked=False)
    comments = Comment.objects.filter(blog=blog, status='visible', author__user_table__is_blocked=False)
    
    if request.method == 'POST' and 'comment' in request.POST:
        # Handle the submission of a new comment
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('view_blog', blog_id=blog.id)
    else:
        comment_form = CommentForm()

    return render(request, 'userpanel/view_blog.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})


@login_required(login_url='/404/')
def add_blog(request):
    # Prevent blocked users from adding new blogs
    if request.user.user_table.is_blocked:
        messages.error(request, 'Your account is blocked. You cannot add new blogs.')
        return redirect('user_home')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog added successfully.')
            return redirect('user_home')
    else:
        form = BlogForm()

    return render(request, 'userpanel/add_blog.html', {'form': form})


@login_required(login_url='/404/')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    # Prevent blocked users from editing their blogs
    if request.user.user_table.is_blocked:
        messages.error(request, 'Your account is blocked. You cannot edit your blogs.')
        return redirect('my_blog')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.status = request.POST.get('status')
            blog.save()
            messages.success(request, 'Blog updated successfully.')
            return redirect('my_blog')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'userpanel/edit_blog.html', {'form': form, 'blog': blog})


@login_required(login_url='/404/')
def add_comment(request, blog_id):
    # Handle the addition of a new comment to a blog
    blog = get_object_or_404(Blog, id=blog_id, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.status = 'visible'
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('view_blog', blog_id=blog.id)
    else:
        form = CommentForm()

    return render(request, 'userpanel/view_blog.html', {'form': form, 'blog': blog})


@login_required(login_url='/404/')
def edit_comment(request, comment_id):
    # Handle the editing of a user's own comment
    comment = get_object_or_404(Comment, id=comment_id, author=request.user, status='visible')
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('view_blog', blog_id=comment.blog.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'userpanel/edit_comment.html', {'form': form, 'comment': comment})


@login_required(login_url='/404/')
def confirm_delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully.')
        return redirect('my_blog')

    return render(request, 'userpanel/confirm_delete_blog.html', {'blog': blog})

@login_required(login_url='/404/')
def delete_comment(request, comment_id):
    # Handle the deletion of a comment
    comment = get_object_or_404(Comment, id=comment_id)
    blog_id = comment.blog.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('view_blog', blog_id=blog_id)

    return render(request, 'userpanel/delete_comment.html', {'comment': comment})


@login_required(login_url='/404/')
def my_blog(request):
    section = request.GET.get('section', 'publish')

    # Get or create User_Table
    user_table, created = User_Table.objects.get_or_create(user=request.user)

    # Prevent blocked users from accessing their blog list
    if user_table.is_blocked:
        messages.error(request, 'Your account is blocked. You cannot manage your blogs.')
        return redirect('user_home')

    published_blogs = Blog.objects.filter(author=request.user, status='published').order_by('-created_at')
    draft_blogs = Blog.objects.filter(author=request.user, status='draft').order_by('-created_at')

    return render(request, 'userpanel/my_blogs.html', {
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'section': section,
    })


@login_required(login_url='/404/')
def reset_password(request):
    # Handle the user's password change request
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'userpanel/reset_password.html', {'form': form})


@login_required(login_url='/404/')
def edit_profile(request, user_id):
    # Handle the editing of the user's profile
    user_profile = get_object_or_404(User_Table, user__id=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Update the User model fields
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()

            # Save the UserProfile model
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_home')
    else:
        form = UserProfileForm(instance=user_profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username,
        })

    return render(request, 'userpanel/edit_profile.html', {'form': form})


@login_required
def sign_out(request):
    # Log out the user and redirect to the home page
    logout(request)
    return redirect('home')

@login_required(login_url='/404/')
def view_user_profile(request, user_id):
    # View another user's profile and their published blogs
    user_profile = get_object_or_404(User_Table, user__id=user_id)
    blogs = Blog.objects.filter(author=user_profile.user, status='published').order_by('-created_at')
    return render(request, 'userpanel/view_profile.html', {'User_profile': user_profile, 'blogs': blogs})
