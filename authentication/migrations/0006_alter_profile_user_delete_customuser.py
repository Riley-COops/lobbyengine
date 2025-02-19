# Generated by Django 5.1.4 on 2025-02-10 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_customuser_groups_and_more'),
        ('message', '0002_alter_messages_recipient_alter_messages_sender'),
        ('notification', '0002_alter_notification_user'),
        ('organisation', '0004_alter_organisation_user'),
        ('post', '0002_alter_post_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
