from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'attendance_tracking_db',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'db',
    'PORT': '5432',
}