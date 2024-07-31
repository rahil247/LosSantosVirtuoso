from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personality = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user.username} - {self.personality} - {self.created_at}"
    

class Message(models.Model):
    # message_id = models.AutoField(primary_key=True)
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.role}: {self.text} ({self.timestamp})"

# class History(models.Model):
#     # message_id = models.AutoField(primary_key=True)
#     chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
#     role = models.CharField(max_length=50)
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name