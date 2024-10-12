from django.urls import path
from .views import user_home, view_user_profile, add_blog, edit_profile, view_blog, edit_blog, user_blog_list, my_blog, reset_password, add_comment, edit_comment, delete_comment, sign_out,confirm_delete_blog

urlpatterns = [
    path('', user_home, name='user_home'),
    path('add_blog/', add_blog, name='add_blog'),
    path('add_comment/<int:blog_id>/', add_comment, name='add_comment'),
    path('blog/<int:blog_id>/', view_blog, name='view_blog'),
    path('blog_list/', user_blog_list, name='user_blog_list'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('edit_blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('my_blog/', my_blog, name='my_blog'),
    path('blog/<int:blog_id>/delete/',confirm_delete_blog, name='confirm_delete_blog'),
    path('profile/<int:user_id>/', view_user_profile, name='view_user_profile'),
    path('reset_password/', reset_password, name='user_reset_password'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('sign_out/', sign_out, name='sign_out'),
]
