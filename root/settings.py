"""
Django settings

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, False),
    ENV=(str, 'dev'),
    CELERY_ALWAYS_EAGER=(bool, False),
    SECRET_KEY=(str, 'TODO_RANDOM'),
    LOGGING_LEVEL=(str, 'INFO'),
    KAFKA_GROUP=(str, 'Group'),
    KAFKA_BOOTSTRAP_SERVERS=(str, 'KAFKA_BROKERS'),
    KAFKA_SECURITY_PROTOCOL=(str, 'SASL_SSL'),
    KAFKA_SASL_MECHANISMS=(str, 'SASL_MECHANISMS'),
    KAFKA_SASL_USERNAME=(str, 'SASL_USERNAME'),
    KAFKA_SASL_PASSWORD=(str, 'SASL_PASSWORD'),
    CACHE_URL=(str, 'redis://redis/0'),
)

env.read_env(env.str('ENV_PATH', '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_DEV = env('ENV') == 'dev'

IS_PRODUCTION = env('ENV') == 'prod'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

LOCAL_APPS = [
    # 'app_name',
    'events',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'corsheaders',

    *LOCAL_APPS,

    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'root.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Kafka
KAFKA_GROUP = env('KAFKA_GROUP')
KAFKA_BOOTSTRAP_SERVERS = env('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_SECURITY_PROTOCOL = env('KAFKA_SECURITY_PROTOCOL')
KAFKA_SASL_MECHANISMS = env('KAFKA_SASL_MECHANISMS')
KAFKA_SASL_USERNAME = env('KAFKA_SASL_USERNAME')
KAFKA_SASL_PASSWORD = env('KAFKA_SASL_PASSWORD')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'root.common.drf_exception_handler.drf_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

DATABASES = {
    'default': env.db()
}

CACHES = {
    'default': env.cache(),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOGGING_LEVEL'),
    },
    'loggers': {
        'environ': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

if not IS_DEV:

    for app in LOCAL_APPS:
        app_config = {
            'handlers': ['console'],
            'level': env('LOGGING_LEVEL'),
            'propagate': False,
        }
        LOGGING['loggers'][app] = app_config

CORS_ALLOW_ALL_ORIGINS = True

# Redis and Celery Config
CELERY_BROKER_URL = env('CELERY_BROKER_URL')

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
