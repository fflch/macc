# MACC

Deploy:

    cp .pg.env.sample .pg.env
    cp .env.sample .env
    python manage.py migrate
    python manage.py runserver
