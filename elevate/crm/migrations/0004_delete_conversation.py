# Generated by Django 4.2.7 on 2024-07-25 09:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0003_rename_character_conversation_personality_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Conversation",
        ),
    ]
