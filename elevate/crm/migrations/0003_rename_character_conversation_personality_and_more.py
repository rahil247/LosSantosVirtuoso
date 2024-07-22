# Generated by Django 4.2.7 on 2024-07-20 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0002_conversation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="conversation",
            old_name="character",
            new_name="personality",
        ),
        migrations.RenameField(
            model_name="conversation",
            old_name="message",
            new_name="text",
        ),
        migrations.AddField(
            model_name="conversation",
            name="role",
            field=models.CharField(default="unknown", max_length=50),
        ),
    ]
