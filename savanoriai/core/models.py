from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=255)


class District(models.Model):
    name = models.CharField(max_length=255)


class Volunteer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    city = models.ForeignKey(City, verbose_name=_("Miestas"))
    district = models.ForeignKey(District, verbose_name=_("Mikrorajonas"), null=True, blank=True)
    phone = models.CharField(verbose_name=_("Telefonas"), max_length=255)
    shift = models.CharField(verbose_name=_("Pamaina"), max_length=255)
    experience = models.IntegerField(verbose_name=_("Patirtis"), blank=True)
