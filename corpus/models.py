from django.db import models
from macc.models import TimeStampedModel

from django.utils.translation import gettext_lazy


class Author(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('autor')
        verbose_name_plural = gettext_lazy('autores')

    first_name = models.CharField(
        max_length=80, verbose_name=gettext_lazy('nome'))
    last_name = models.CharField(
        max_length=255, verbose_name=gettext_lazy('sobrenome'))

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Translator(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('tradutor')
        verbose_name_plural = gettext_lazy('tradutores')

    first_name = models.CharField(
        max_length=80, verbose_name=gettext_lazy('nome'))
    last_name = models.CharField(
        max_length=255, verbose_name=gettext_lazy('sobrenome'))

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Work(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('obra')
        verbose_name_plural = gettext_lazy('obras')

    year = models.PositiveIntegerField(
        null=True, verbose_name=gettext_lazy('ano'))
    title = models.CharField(
        max_length=255, verbose_name=gettext_lazy('título'))
    code = models.CharField(
        max_length=20, verbose_name=gettext_lazy('código'), unique=True)
    authors = models.ManyToManyField(
        Author, verbose_name=gettext_lazy('autores'))

    def __str__(self) -> str:
        return self.title


class Place(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('local')
        verbose_name_plural = gettext_lazy('locais')

    city = models.CharField(
        max_length=255, null=True, verbose_name=gettext_lazy('cidade'))
    state_province = models.CharField(
        max_length=255, null=True, verbose_name=gettext_lazy('estado/província'))
    country = models.CharField(
        max_length=255, verbose_name=gettext_lazy('país'))

    def __str__(self) -> str:
        return ", ".join(filter(lambda v: v is not None, [self.city, self.state_province, self.country]))


class Publisher(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('editora')
        verbose_name_plural = gettext_lazy('editoras')

    name = models.CharField(max_length=255, verbose_name=gettext_lazy('nome'))
    place = models.ForeignKey(
        Place, null=True, blank=True, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.name


class Collection(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('coletânea')
        verbose_name_plural = gettext_lazy('coletâneas')

    year = models.PositiveIntegerField(verbose_name=gettext_lazy('ano'))
    title = models.CharField(
        max_length=255, verbose_name=gettext_lazy('título'))
    code = models.CharField(
        max_length=20, verbose_name=gettext_lazy('código'), unique=True)
    authors = models.ManyToManyField(
        Translator, blank=True, verbose_name=gettext_lazy('autores'))
    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.RESTRICT, verbose_name=gettext_lazy('editora'))

    def __str__(self) -> str:
        return self.title


class Translation(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('tradução')
        verbose_name_plural = gettext_lazy('traduções')

    year = models.PositiveIntegerField(
        null=True, verbose_name=gettext_lazy('ano'))
    title = models.CharField(
        max_length=255, verbose_name=gettext_lazy('título'))
    code = models.CharField(
        max_length=20, verbose_name=gettext_lazy('código'), unique=True)
    work = models.ForeignKey(
        Work, on_delete=models.RESTRICT, verbose_name=gettext_lazy('original'))
    authors = models.ManyToManyField(
        Translator, blank=True, verbose_name=gettext_lazy('autores'))
    collection = models.ForeignKey(
        Collection, null=True, blank=True, on_delete=models.RESTRICT, verbose_name=gettext_lazy('coletânea'))
    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.RESTRICT, verbose_name=gettext_lazy('editora'))

    def __str__(self) -> str:
        return self.title


class OriginalFragment(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('fragmento original')
        verbose_name_plural = gettext_lazy('fragmentos originais')
        db_table = 'corpus_original_fragment'

    work = models.ForeignKey(
        Work, on_delete=models.RESTRICT, verbose_name=gettext_lazy('obra'))
    fragment = models.TextField(verbose_name=gettext_lazy('fragmento'))


class TranslatedFragment(TimeStampedModel):
    class Meta:
        verbose_name = gettext_lazy('fragmento traduzido')
        verbose_name_plural = gettext_lazy('fragmentos traduzidos')
        db_table = 'corpus_translated_fragment'

    work = models.ForeignKey(
        Translation, on_delete=models.RESTRICT, verbose_name=gettext_lazy('tradução'))
    fragment = models.TextField(verbose_name=gettext_lazy('fragmento'))
    original = models.ForeignKey(
        OriginalFragment, on_delete=models.RESTRICT, verbose_name=gettext_lazy('original'))
