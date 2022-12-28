# MACC

Deploy:

    cp .pg.env.sample .pg.env
    cp .env.sample .env
    python manage.py collectstatic
    python manage.py migrate
    python manage.py runserver

Generate secret key:

    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Create a first user:

    python manage.py createsuperuser
