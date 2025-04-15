# Generated by Django 5.2 on 2025-04-13 21:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='')),
                ('category', models.TextField()),
                ('brand', models.TextField(blank=True)),
                ('color', models.TextField(blank=True)),
                ('season', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('bottoms', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outfits_bottoms', to='project.clothingitem')),
                ('hat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outfits_hat', to='project.clothingitem')),
                ('jacket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outfits_jacket', to='project.clothingitem')),
                ('shirt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outfits_shirt', to='project.clothingitem')),
                ('shoes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outfits_shoes', to='project.clothingitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('date', models.DateTimeField()),
                ('location', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('outfit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.outfit')),
            ],
        ),
    ]
