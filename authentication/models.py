from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class Profile(models.Model):
    from organisation.models import Address

    CATEGORY_CHOICE={
       'PERSONNEL': 'Personnel',
        'INVESTOR ': 'Investor'
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE, default='PERSONNEL')
    dob =  models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=100, null=True)
    job_description = models.CharField(max_length=100, null=False)




    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def registration_email(sender, instance, created,**kwargs):
    from django.core.mail import send_mail
    from django.conf import settings
    if created:
        send_mail(
            subject="Registration Successful",
            message = f"Dear {instance.email}, you have been successfully registered on Lobby ",
            from_mail = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [instance.email],
            fail_silently = False,
        )


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Handle the case where a Profile instance doesn't exist
        pass