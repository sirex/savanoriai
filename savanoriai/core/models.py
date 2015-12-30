from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Miestas")
        verbose_name_plural = _("Miestai")

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, null=True, editable=False)

    class Meta:
        verbose_name = _("Mikrorajonas")
        verbose_name_plural = _("Mikrorajonai")

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    city = models.ForeignKey(City, verbose_name=_("Miestas"))
    district = models.ForeignKey(District, verbose_name=_("Mikrorajonas"), null=True, blank=True)
    phone = models.CharField(verbose_name=_("Telefonas"), max_length=255)
    shift = models.CharField(verbose_name=_("Pamaina"), max_length=255)
    experience = models.IntegerField(verbose_name=_("Patirtis"), blank=True)

    class Meta:
        verbose_name = _("Savanoris")
        verbose_name_plural = _("Savanoriai")

    def __str__(self):
        return self.user
