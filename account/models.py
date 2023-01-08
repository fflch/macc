from django.contrib.auth.models import AbstractUser
from django.db import models
from macc.models import TimeStampedModel
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    email = models.EmailField(unique=True)
    consent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(TimeStampedModel):
    CHOICES = {
        'gender': [
            ('', ''),
            ('M', gettext_lazy('Masculino')),
            ('F', gettext_lazy('Feminino')),
            ('NB', gettext_lazy('Não-binário')),
            ('O', gettext_lazy('Outro')),
        ]
    }

    class Meta:
        verbose_name = gettext_lazy('perfil')
        verbose_name_plural = gettext_lazy('perfis')

    user = models.OneToOneField(
        User, on_delete=models.RESTRICT, verbose_name=gettext_lazy('usuario'))
    birth_date = models.DateField(
        verbose_name=gettext_lazy('data de nascimento'))
    country = CountryField(default='BR', verbose_name=gettext_lazy('país'))
    gender = models.CharField(max_length=2, null=True, blank=True,
                              verbose_name=gettext_lazy('gênero'))
    occupation = models.CharField(max_length=80,
                                  null=True, blank=True, verbose_name=gettext_lazy('profissão'))
    education_institution = models.BooleanField(
        default=False, verbose_name=gettext_lazy('vínculo com instituição de ensino?'))

    def __str__(self):
        return self.user.username
