"""
Django settings for {{ cookiecutter.project_slug }}_microservice project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from {{ cookiecutter.project_slug }}_service import logger
from {{ cookiecutter.project_slug }}_service.config import BaseConfig, SentryConfig


class Config(BaseConfig):
    pass


CONFIG: Config = Config.from_env()


######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = CONFIG.SECRET_KEY
DEBUG = CONFIG.DEBUG
ROOT_URLCONF = '{{ cookiecutter.project_slug }}_service.urls'
WSGI_APPLICATION = '{{ cookiecutter.project_slug }}_service.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

######################################################################
# Domain
######################################################################

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = CONFIG.CSRF_TRUSTED_ORIGINS
if CONFIG.ALLOW_CORS:
    CORS_ORIGIN_ALLOW_ALL = True

######################################################################
# Apps
######################################################################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'django_structlog',
    '{{ cookiecutter.app_name }}',
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

if CONFIG.ALLOW_CORS:
    INSTALLED_APPS.append('corsheaders')
    MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '{{ cookiecutter.project_slug }}_service' / 'templates'],
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


######################################################################
# Databases
######################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': CONFIG.DJANGO_DB_NAME,
        'USER': CONFIG.DJANGO_DB_USER,
        'PASSWORD': CONFIG.DJANGO_DB_PASSWORD,
        'HOST': CONFIG.DJANGO_DB_HOST,
        'PORT': CONFIG.DJANGO_DB_PORT,
    }
}


######################################################################
# Authentication
######################################################################


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
)

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

######################################################################
# LOGGING
######################################################################

LOGGING = logger.get_config(to_json=CONFIG.LOGGING_JSON, level=CONFIG.LOGGING_LEVEL)


if CONFIG.LOGGING_REQUESTS:
    MIDDLEWARE.append('django_structlog.middlewares.RequestMiddleware')

######################################################################
# Localization
######################################################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/GMT-1'

USE_L10N = True

USE_I18N = True

USE_TZ = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]

LOCALE_PATHS = [BASE_DIR / '{{ cookiecutter.project_slug }}_service' / 'locale']


######################################################################
# Static
######################################################################


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / '{{ cookiecutter.project_slug }}_service' / 'media/'

###########################
## Sentry
###########################
if CONFIG.SENTRY_ACTIVATE:
    SentryConfig.from_env().setup_sentry(CONFIG.ENV)
else:
    print('Sentry deactivated, change env SENTRY_ACTIVATE to activate')
