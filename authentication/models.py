from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

@receiver(post_save, sender=CustomUser)
def registration_email(sender, instance, created,**kwargs):
    from django.core.mail import send_mail
    from django.conf import settings
    if created:
        send_mail(
            subject="Registration Successful",
            message = f"Dear {instance.email}, you have been successfully registered on Lobby ",
            from_mail = settings.DEFAULT_FROM_MAIL,
            recipient_list = [instance.email],
            fail_silently = False,
        )

class Profile(models.Model):
    from organisation.models import Address

    CATEGORY_CHOICE={
       'PERSONNEL': 'Personnel',
        'INVESTOR ': 'Investor'
    }

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE, default='PERSONNEL')
    dob =  models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=100, null=True)
    job_description = models.CharField(max_length=100, null=False)




    def __str__(self):
        return self.user



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Handle the case where a Profile instance doesn't exist
        pass