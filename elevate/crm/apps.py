# Importing AppConfig from django.apps. This class is used to configure application settings.
from django.apps import AppConfig

# Defining a configuration class for the CRM application.
# This class inherits from AppConfig, which is the base class for application configurations.
class CrmConfig(AppConfig):
    # Setting the default type for auto-incrementing primary keys to BigAutoField.
    # BigAutoField is a 64-bit integer, which allows for a larger range of values.
    default_auto_field = "django.db.models.BigAutoField"
    
    # Specifying the name of the application. This is used by Django to identify the app.
    # The name should be the same as the directory name where this file is located.
    name = "crm"
