# Generated by Django 5.2 on 2025-04-30 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_outfit_occasion_outfit_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='occasion',
            field=models.CharField(blank=True, choices=[('casual', 'Casual'), ('formal', 'Formal'), ('party', 'Party'), ('work', 'Work'), ('vacation', 'Vacation')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='season',
            field=models.CharField(blank=True, choices=[('fall_winter', 'Fall/Winter'), ('spring_summer', 'Spring/Summer'), ('all_year', 'All Year')], max_length=20, null=True),
        ),
    ]
