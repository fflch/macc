from macc.settings.base import *

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
        'level': 'WARNING',
    },
}

CSRF_TRUSTED_ORIGINS = ["https://macc.fflch.usp.br", "https://www.macc.fflch.usp.br"]
