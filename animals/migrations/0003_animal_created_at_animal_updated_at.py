# Generated by Django 4.1 on 2022-08-22 01:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0002_rename_trait_animal_traits"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="animal",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
