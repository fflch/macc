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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'asyncio': {
            'level': 'WARNING',
        }
    },
}
