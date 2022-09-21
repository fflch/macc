from django.db import models
from macc.models import TimeStampedModel

from django.utils.translation import gettext_lazy

class BaseAuthor(TimeStampedModel):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=80, verbose_name=gettext_lazy('nome'))
    last_name = models.CharField(max_length=255, verbose_name=gettext_lazy('sobrenome'))

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Author(BaseAuthor):
    class Meta:
        verbose_name = gettext_lazy('autor')
        verbose_name_plural = gettext_lazy('autores')

class Translator(BaseAuthor):
    class Meta:
        verbose_name = gettext_lazy('tradutor')
        verbose_name_plural = gettext_lazy('tradutores')

class Work(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('obra')
        verbose_name_plural = gettext_lazy('obras')

    title = models.CharField(max_length=255, verbose_name=gettext_lazy('título'))
    code = models.CharField(max_length=20, verbose_name=gettext_lazy('código'), unique=True)
    authors = models.ManyToManyField(Author, verbose_name=gettext_lazy('autores'))

    def __str__(self) -> str:
        return self.title
