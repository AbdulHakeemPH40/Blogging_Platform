from django.urls import path
from .views import admin_home, user_list,view_user,blog_list,reset_password,admin_view_blog,admin_hide_blog,admin_show_blog,admin_hide_comment,admin_show_comment,view_user,block_user,unblock_user,admin_sign_out,admin_view_user_profile


urlpatterns = [
    path('admin_home/', admin_home, name='admin_home'),
    path('user_list/', user_list, name='user_list'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
    path('reset_password/', reset_password, name='reset_password'),
    path('blog_list/', blog_list, name='blog_list'),
    path('view_blog/', admin_view_blog, name='admin_view_blog'),
    path('admin_sign_out/', admin_sign_out, name='admin_sign_out'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('view_blog/<int:blog_id>/', admin_view_blog, name='admin_view_blog'),
    path('hide_blog/<int:blog_id>/', admin_hide_blog, name='admin_hide_blog'),
    path('show_blog/<int:blog_id>/', admin_show_blog, name='admin_show_blog'),
    path('hide_comment/<int:comment_id>/', admin_hide_comment, name='admin_hide_comment'),
    path('show_comment/<int:comment_id>/', admin_show_comment, name='admin_show_comment'),
    path('user/<int:user_id>/', view_user, name='admin_view_user_profile'),
    path('user/<int:user_id>/', admin_view_user_profile, name='admin_view_user_profile'),
   
     
]