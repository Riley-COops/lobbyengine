from django.db import models
from authentication.models import CustomUser

class Post(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)  # Text content
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='text')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.username}- {self.content_type}"
