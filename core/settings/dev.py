from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'attendance_db_dev',
    'USER': 'postgres',
    'PASSWORD': 'dev_password',
    'HOST': 'localhost',
    'PORT': '5432',
}