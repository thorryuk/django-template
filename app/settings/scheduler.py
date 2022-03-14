from celery.schedules import crontab

from kombu import Queue, Exchange

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.dirname(__name__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$%v6=xh68!0^yg5#flgun&7raf(&*c)-c!!%zyurp9gj3g(mtq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'django_celery_beat',
    'backend',
    'scheduler',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_pln',
        'USER': 'pln',
        'PASSWORD': 'coba2128',
        'HOST': 'localhost',
        'PORT': '5431',
        'CONN_MAX_AGE': 300
    }
}

LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    },
}

TRES_HOLD_RETRY = 2

# BROKER CONFIGURATION #
BROKER_URL = 'amqp://rabbitmq:qnJzJ46d1RypmwYq@172.20.0.2:5672//'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 600
CELERY_TRACK_STARTED = False

# CELERY TASK QUEUE CONFIG
CELERY_DEFAULT_QUEUE = 'celery'
CELERY_IMPORTS = ('scheduler.tasks',)

CELERY_QUEUES = {
    Queue('celery', Exchange('celery'), routing_key='celery'),
    Queue('beat', Exchange('beat'), routing_key='beat'),
}

CELERY_ROUTES = {
    'scheduler.tasks.mail': {'queue': 'celery', 'routing_key': 'celery'},
    # 'scheduler.tasks.check_status_job': {'queue': 'beat', 'routing_key': 'beat'},
}

CELERYBEAT_SCHEDULE = {
    # 'internal_approval_reminde': {
    #     'task': 'scheduler.tasks.check_status_job',
    #     'schedule': crontab(minute=0, hour=0, day_of_week='*')
    # }
}


# DEFAULT_EMAIL_HOST = 'smtp.gmail.com'
# DEFAULT_EMAIL_PORT = 465
# DEFAULT_EMAIL_HOST_USER = 'me.gomzy@gmail.com'
# DEFAULT_EMAIL_HOST_PASSWORD = 'z9%~}+6M^FeDDsT/'
# DEFAULT_EMAIL_USE_TLS = True

# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD = 'z9%~}+6M^FeDDsT/'
# EMAIL_HOST_USER = 'me.gomzy@gmail.com'
# EMAIL_PORT = 587
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# DEFAULT_EMAIL_HOST = 'mail.hseo.co.id'
# DEFAULT_EMAIL_PORT = 587
# DEFAULT_EMAIL_HOST_USER = 'ppa@hseo.co.id'
# DEFAULT_EMAIL_HOST_PASSWORD = 'CarbonX12020##'
# DEFAULT_EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'mail.hseo.co.id'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'ppa@hseo.co.id'
# EMAIL_HOST_PASSWORD = 'CarbonX12020##'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


DEFAULT_EMAIL_HOST = 'smtp.gmail.com'
DEFAULT_EMAIL_PORT = 465
DEFAULT_EMAIL_HOST_USER = 'thoriq.mailtesting@gmail.com'
DEFAULT_EMAIL_HOST_PASSWORD = 'coba2128'
DEFAULT_EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'thoriq.mailtesting@gmail.com'
EMAIL_HOST_PASSWORD = 'coba2128'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LINK_NIPPON_CMS = 'http://nippon.h-seo.com/signin/'
LINK_NIPPON_FRONTEND = 'http://fenippon.h-seo.com/'
