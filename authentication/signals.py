from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_message(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Our Platform"
        message = f"Hello {instance.email},\n\nThank you for registering on our platform. We are excited to have you on board!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)
