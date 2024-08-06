"""
ASGI config for elevate project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# Importing the os module, which provides a way to interact with the operating system.
import os

# Importing get_asgi_application from django.core.asgi.
# This function returns an ASGI callable for the project.
from django.core.asgi import get_asgi_application

# Setting the default settings module for the 'elevate' project.
# 'elevate.settings' refers to the settings.py file in the elevate project directory.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevate.settings")

# Creating an ASGI application instance using the settings module specified above.
# This instance will be used to handle ASGI requests.
application = get_asgi_application()



