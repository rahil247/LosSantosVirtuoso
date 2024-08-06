# Import the admin module from Django to register models for the admin interface
from django.contrib import admin

# Import the models that you want to register with the admin interface
from .models import ChatSession, Message, Contact

# Register the ChatSession model with the admin interface
admin.site.register(ChatSession)

# Register the Message model with the admin interface
admin.site.register(Message)

# Register the Contact model with the admin interface
admin.site.register(Contact)
