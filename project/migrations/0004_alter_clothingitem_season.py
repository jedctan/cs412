# Generated by Django 5.2 on 2025-04-29 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_clothingitem_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='season',
            field=models.CharField(blank=True, choices=[('fall_winter', 'Fall/Winter'), ('spring_summer', 'Spring/Summer'), ('all_year', 'All Year')], max_length=20),
        ),
    ]
