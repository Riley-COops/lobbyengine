from django.db import models
from authentication.models import CustomUser
# Create your models here.

class Messages(models.Model):
    sender= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_message')
    recipient = models.ForeignKey(CustomUser, related_name='recieved_message', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'