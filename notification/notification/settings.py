"""
Django settings for notification project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Load environment variables from .env file
load_dotenv()



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Load DEBUG from .env
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)    

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')


# constants and .env variables
sms_rate_limit = os.getenv('SMS_RATELIMIT_PER_MINUTE', 10)  


# SMTP settings
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')  # SMTP host
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))  # SSMTP port
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') 
SMS_API_KEY = os.getenv('SMS_API_KEY')  
SMS_API_HEADER_FIELD = 'X-GeezSMS-Key'
SMS_API_URL = 'https://api.geezsms.com/api/v1/sms/send'
SMS_BULK_API_URL = 'https://api.geezsms.com/api/v1/sms/send/bulk'
SMS_SHORT_CODE = '' 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_api_key',
    'rest_framework.authtoken',
    'email_notification',
    'sms_notification',
    'monitor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notification.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'notification.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework_api_key.permissions.HasAPIKey',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_RATES': {
        'sms': f'{sms_rate_limit}/minute',  
    },
}


SPECTACULAR_SETTINGS = {
    'TITLE':  'Bita notification service',
    'DESCRIPTION': 'API documentation for my project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # Hide the schema endpoint
   "APPEND_COMPONENTS": {
        "securitySchemes": {"ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"}}
    },
    "SECURITY": [{"ApiKeyAuth": [],}],
}



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),  
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True, 
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname})- {name}- {message}",
            "style": "{",
        }
    },
}


