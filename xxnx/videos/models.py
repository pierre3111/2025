from django.db import models
from django.contrib.auth.models import User

class MediaType(models.TextChoices):
    VIDEO = 'video', 'Video'
    PHOTO = 'photo', 'Photo'

class Media(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/')
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.VIDEO)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
