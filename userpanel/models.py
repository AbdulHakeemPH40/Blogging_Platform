# models.py

from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class User_Table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')  # Add related_name='blogs'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title



class Comment(models.Model):
    STATUS_CHOICES = [
        ('hidden', 'Hidden'),
        ('visible', 'Visible'),
    ]

    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='visible')

    def __str__(self):
        return self.comment[:20]
