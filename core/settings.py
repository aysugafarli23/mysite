"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # loads the configs from .env
import os


CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/login', 'https://www.your-domain.com']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('django-insecure-*4ok4##@f5zp6^1toj$uy_#tdf%2sy65g8c9(i55+*lzv_dj50'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #My Apps:
    'users',
    'module',
    'dictionary',
    'contact',
    'rest_framework',
    'django_filters',
    'social_django',
    'djstripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                 # Sign in with social apps
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Cookies
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

#Login route
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

#Sign in with social apps
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


# social auth configs for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('703386953476-b02pq8gmoj1lms8i5kcnqjf4t89h1iul.apps.googleusercontent.com'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('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'))

#Stripe configuration
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY","pk_test_51PX8O7Ee6ATWy3dPTPlqOlU0TJz9bISnx3MgYkl8rHIfnMDO4DpppPz7vheR7U5T6he6BhnrMX84UsGOIOifo7OY00y8JUG6Zl")
# STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY","sk_test_51PX8O7Ee6ATWy3dP72TIFrAcaqcFaFOW6P0R9tPescQXCxvgPSt8UHw5ZOjxW6pQKpjzFu7Dr5DESmzsfyZRGsR100cxdm7KBn")
DJSTRIPE_WEBHOOK_SECRET = 'whsec_784668e2972b0114189003dcacc5e278930b5c00d2abfd6e894860707e214aa6'

# Use test keys while in development
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"