# Generated by Django 5.1.5 on 2025-04-01 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="apartment_num",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="voter",
            name="party",
            field=models.CharField(max_length=2),
        ),
    ]
