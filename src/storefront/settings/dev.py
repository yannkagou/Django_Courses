from .common import *

SECRET_KEY = 'django-insecure-0!je*%5($vw)j^+6=+q3&4yup@g87nv_40=x-qsb+hwbqyt9*-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'storefront',
        'USER': 'postgres',
        'PASSWORD': 'yannick1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
