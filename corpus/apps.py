from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class CorpusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corpus'
    verbose_name = 'corpus'
    verbose_name_plural = 'corpora'
