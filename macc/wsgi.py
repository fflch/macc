"""
WSGI config for macc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

SETTINGS_FILE = os.getenv('DJANGO_ENV') or 'base'
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      f'macc.settings.{SETTINGS_FILE}')

application = get_wsgi_application()
