# Generated by Django 5.2 on 2025-05-01 20:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='ProjProfile',
        ),
    ]
