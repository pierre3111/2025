from django.db import models
from django.contrib.auth.models import User

class MediaItem(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def is_video(self):
        return self.media_type == 'video'
    
    def is_image(self):
        return self.media_type == 'image'

class UserEmail(models.Model):
    email = models.EmailField(unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.IntegerField(default=1)
    
    def __str__(self):
        return self.email

class MediaAccess(models.Model):
    user_email = models.ForeignKey(UserEmail, on_delete=models.CASCADE)
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user_email', 'media_item')
        
    def __str__(self):
        return f"{self.user_email} accessed {self.media_item}"