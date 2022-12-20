from macc.settings.base import *

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS += [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar'
]
