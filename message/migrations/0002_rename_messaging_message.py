# Generated by Django 5.0.4 on 2024-05-04 00:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Messaging",
            new_name="Message",
        ),
    ]
