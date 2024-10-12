from django.contrib import admin
from .models import Blog, Comment,User_Table

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(User_Table)