# Importing the WSGI application from the elevate project.
from elevate.wsgi import application

# Assigning the imported WSGI application to the variable 'app'.
# This makes 'app' the WSGI callable for deployment.
app = application

