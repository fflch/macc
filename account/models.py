from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    email = models.EmailField(unique=True)
    consent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.RESTRICT, verbose_name=gettext_lazy('editora'))
    # ano de nascimento
    # país
    # gênero,
    # profissão,
    # vínculo com instituição educacional (sim/não)
    # Estou ciente do termo de responsabilidade

    def __str__(self):
        return self.user.username
