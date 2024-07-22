from django.db import models
from django.contrib.auth.models import User

<<<<<<< Updated upstream
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personality = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
=======
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {'Success' if self.successful else 'Failure'}"

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     additional_field = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.user.username



class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personality = models.CharField(max_length=100)
    role = models.CharField(max_length=50,default="unknown")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.personality} - {self.timestamp}'
    
>>>>>>> Stashed changes
