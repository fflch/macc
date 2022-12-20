"""
ASGI config for macc project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

SETTINGS_FILE = os.getenv('DJANGO_ENV') or 'base'
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      f'macc.settings.{SETTINGS_FILE}')

application = get_asgi_application()
