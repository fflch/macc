from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class WorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'work'
    verbose_name = gettext_lazy('work')
    verbose_name_plural = gettext_lazy('works')
