import os
# import dj_database_url
# from dotenv import load_dotenv
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Setting the base directory for the project. BASE_DIR refers to the directory containing manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(os.path.join(BASE_DIR/".eVar",".env"))
# Secret key for the Django project. This key should be kept secret in production.
SECRET_KEY = 'django-insecure-#eo+&9jk!b%@)me=xdbz6&ses00s$^rr15095%ccn&7)ngf3fi'

# Debug mode setting. Should be set to False in production.
DEBUG = True

# Allowed hosts setting. Specifies the host/domain names that this Django site can serve.
ALLOWED_HOSTS = ['wmc-5-0.onrender.com','127.0.0.1']

# Setting the site ID for the project.
SITE_ID = 2

# Defining the installed applications for the project.
INSTALLED_APPS = [
    "material",  # Material design for Django admin interface.
    "material.admin",  # Material design for Django admin interface.
    "django.contrib.auth",  # Django's authentication framework.
    "django.contrib.contenttypes",  # Django's content type framework.
    "django.contrib.sessions",  # Django's session framework.
    "django.contrib.messages",  # Django's messaging framework.
    "django.contrib.staticfiles",  # Django's static files handling framework.
    "crm",  # Custom CRM application.
    "django.contrib.sites",  # Django's sites framework.
    "allauth",  # Django Allauth for authentication.
    "allauth.account",  # Django Allauth for account management.
    "allauth.socialaccount",  # Django Allauth for social account management.
    "allauth.socialaccount.providers.google",  # Django Allauth for Google social account management.
]

# Configuration for social account providers, specifically Google in this case.
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online"},
        'APP': {
            'client_id': '133402870707-nhuffft968a6jolttuq1b2b6jg42rk3p.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

# Defining the middleware for the project.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security middleware.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session middleware.
    "django.middleware.common.CommonMiddleware",  # Common middleware.
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection middleware.
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentication middleware.
    "django.contrib.messages.middleware.MessageMiddleware",  # Messaging middleware.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection middleware.
    "allauth.account.middleware.AccountMiddleware",  # Allauth account middleware.
    'crm.middleware.NoCacheMiddleware',  # Custom middleware to disable caching.
    # 'django.middleware.timezone.TimeZoneMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# Setting the root URL configuration for the project.
ROOT_URLCONF = "elevate.urls"

# Defining the template settings for the project.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Using Django templates.
        "DIRS": [],  # Directories to search for templates.
        "APP_DIRS": True,  # Whether to look for templates in app directories.
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Adds debug context processor.
                "django.template.context_processors.request",  # Adds request context processor.
                "django.contrib.auth.context_processors.auth",  # Adds auth context processor.
                "django.contrib.messages.context_processors.messages", # Adds messages context processor.
                  'django.template.context_processors.tz',  
            ],
        },
    },
]

# Setting the WSGI application for the project.
WSGI_APPLICATION = "elevate.wsgi.application"

# Defining the database settings for the project.
DATABASES = {
    "default": {
        "URL": "mysql://avnadmin:AVNS_MC9pJexeUopA37T5pAE@mysql-36f76dc3-wmc-5.e.aivencloud.com:12277/defaultdb?ssl-mode=REQUIRED",
        "ENGINE": "django.db.backends.mysql",  # Using MySQL as the database engine.
        "NAME": "defaultdb",  # Database name.
        "USER": "avnadmin",  # Database user.
        "PASSWORD": "AVNS_MC9pJexeUopA37T5pAE",  # Database password.
        "HOST": "mysql-36f76dc3-wmc-5.e.aivencloud.com",  # Database host.
        "PORT": "12277",  # Database port.
    }
}

# DATABASES = {
#     'default' : dj_database_url.config(
#         default = "sqlite:///" + os.path.join(BASE_DIR,"db.sqlite3")
#     )
# }

# The following commented-out section shows a basic database configuration that was previously defined.
# DATABASES["default"] = dj_database_url.parse("postgresql://chatbot_wmc_user:6EMiBvj0z0xY3NHwlCg8WIUzMYt6EWhs@dpg-cqja3maj1k6c739pguag-a.oregon-postgres.render.com/chatbot_wmc")

# Defining the password validation settings for the project.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # Prevents passwords that are too similar to the user's attributes.
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # Enforces a minimum length for passwords.
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # Prevents commonly used passwords.
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # Prevents passwords that are entirely numeric.
    },
]

# Setting the language code for the project.
LANGUAGE_CODE = "en-us"

# Setting the time zone for the project.
TIME_ZONE = "UTC"

# Enabling internationalization.
USE_I18N = True

# Enabling time zone support.
USE_TZ = True

# Setting the URL for static files.
STATIC_URL = "static/"

# Defining the static files directory.
STATIC_FILES = os.path.join(BASE_DIR, 'static')

# Defining the static root directory for static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Setting the default auto field type for the project.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Defining the API keys for Razorpay.
RAZORPAY_API_KEY = 'rzp_live_2DWZBQ5mIimbcX'
RAZORPAY_API_SECRET_KEY = 'jy8T9rW0uIhp25NXxy67IhVE'

# Defining the authentication backends for the project.
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Default authentication backend.
    "allauth.account.auth_backends.AuthenticationBackend"  # Allauth authentication backend.
)
# changed LOGIN_REDIRECT_URL from '/' to 'welcome'
LOGIN_REDIRECT_URL = "welcome"
LOGOUT_REDIRECT_URL = "/index/"

LOGIN_URL = '/login/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True

TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
USE_I18N = True
USE_L10N = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# import os

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
