"""
Settings for django-tiles tests and sphinx build
"""

import os
SECRET_KEY = 'testkey'

INSTALLED_APPS = (
    'wms',
)

DATABASES = {
    'default': {
        'ENGINE':   'django.contrib.gis.db.backends.postgis',
        'USER':     os.environ.get('DB_USER', 'postgres'),
        'HOST':     os.environ.get('DB_HOST', 'localhost'),
        'NAME':     os.environ.get('DB_NAME', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'PORT':     os.environ.get('DB_PORT', 'postgres'),
    }
}

DEBUG = True
