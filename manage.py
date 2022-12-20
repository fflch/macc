#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from glob import glob
from dotenv import load_dotenv

env_files = [
    '.env',
    '.pg.env',
]


def main():
    """Run administrative tasks."""
    for env_file in env_files:
        load_dotenv(env_file)

    SETTINGS_FILE = os.getenv('DJANGO_ENV') or 'base'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          f'macc.settings.{SETTINGS_FILE}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
