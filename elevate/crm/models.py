from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Defining a model for chat sessions.
class ChatSession(models.Model):
    # A foreign key relationship to the User model.
    # If a user is deleted, all related chat sessions will also be deleted (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # A field to store the personality type or identifier for the chat session.
    personality = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user.username} - {self.personality} - {self.created_at}"
    
    # A field to automatically record the creation time of the chat session.
    # Uncomment the following line if you want to include the creation timestamp.
    # created_at = models.DateTimeField(auto_now_add=True)

# Defining a model for messages within a chat session.
class Message(models.Model):
    # A foreign key relationship to the ChatSession model.
    # If a chat session is deleted, all related messages will also be deleted (CASCADE).
    # The related_name attribute allows reverse lookup from ChatSession to Message.
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    # A field to store the role of the message sender (e.g., user, bot).
    role = models.CharField(max_length=50)
    # A field to store the content of the message.
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.role}: {self.text} ({self.timestamp})"

# Defining a model for storing contact information.
class Contact(models.Model):
    # A field to store the contact's name.
    name = models.CharField(max_length=255)
    # A field to store the contact's email address.
    email = models.EmailField()
    # A field to store the contact's message.
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # A field to automatically record the creation time of the contact entry.
    # created_at = models.DateTimeField(auto_now_add=True)

    # A string representation of the Contact model, returning the contact's name.
    def __str__(self):
        return self.name
