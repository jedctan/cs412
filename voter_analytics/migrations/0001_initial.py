# Generated by Django 5.1.5 on 2025-04-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_name", models.TextField()),
                ("first_name", models.TextField()),
                ("dob", models.DateField()),
                ("registration_date", models.DateField()),
                ("party", models.TextField()),
                ("precinct_num", models.IntegerField()),
                ("voter_score", models.IntegerField()),
                ("street_num", models.IntegerField()),
                ("street_name", models.TextField()),
                ("apartment_num", models.IntegerField()),
                ("zip_code", models.IntegerField()),
                ("v20state", models.BooleanField()),
                ("v21town", models.BooleanField()),
                ("v21primary", models.BooleanField()),
                ("v22general", models.BooleanField()),
                ("v23town", models.BooleanField()),
            ],
        ),
    ]
