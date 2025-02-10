from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Messages(models.Model):
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    recipient = models.ForeignKey(User, related_name='recieved_message', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.userbane}:{self.content[:50]} at {self.timestamp}'