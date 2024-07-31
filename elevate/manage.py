#!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevate.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == "__main__":
#     main()

"""Django's command-line utility for administrative tasks."""

import os  # Importing the os module to interact with the operating system.
import sys  # Importing the sys module to interact with the Python interpreter.

def main():
    """Run administrative tasks."""
    # Setting the default settings module for the 'elevate' project.
    # 'elevate.settings' refers to the settings.py file in the elevate project directory.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevate.settings")
    try:
        # Importing the execute_from_command_line function from django.core.management.
        # This function is used to execute Django command-line utilities.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed or cannot be imported, an ImportError is raised.
        # This exception block provides a user-friendly error message.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Executing the command-line utility with the arguments passed to the script.
    execute_from_command_line(sys.argv)

# If this script is run directly (rather than imported as a module), the main() function is called.
if __name__ == "__main__":
    main()
