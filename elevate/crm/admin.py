from django.contrib import admin

# Register your models here.
from .models import ChatSession, Message,Contact


# admin.site.register(Contact)
# admin.site.register(LoginAttempt)
admin.site.register(ChatSession)
# admin.site.register(History)
admin.site.register(Message)
admin.site.register(Contact)