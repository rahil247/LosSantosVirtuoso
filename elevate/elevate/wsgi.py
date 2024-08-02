"""
WSGI config for elevate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevate.settings")

# application = get_wsgi_application()

# app = application

import os  # Importing the os module to interact with the operating system.

from django.core.wsgi import get_wsgi_application  # Importing get_wsgi_application to get the WSGI application.
import os
from dotenv import load_dotenv

load_dotenv()
# Setting the default settings module for the 'elevate' project.
# 'elevate.settings' refers to the settings.py file in the elevate project directory.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevate.settings")

# Creating a WSGI application instance using the settings module specified above.
# This instance will be used to handle WSGI requests.
application = get_wsgi_application()

# Assigning the WSGI application instance to a variable named 'app'.
# This can be useful for some WSGI servers or configurations that expect 'app'.
app = application
