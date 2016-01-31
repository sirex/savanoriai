from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Place(models.Model):
    county = models.CharField(verbose_name=_("Apskritis"), max_length=255)
    municipality = models.CharField(verbose_name=_("Savivaldybė"), max_length=255)
    eldership = models.CharField(verbose_name=_("Seniūnija"), max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    osm_id = models.CharField(max_length=20)
    place = models.CharField(verbose_name=_("Gyvenvietė"), max_length=255)
    population = models.IntegerField(null=True)
    type = models.CharField(max_length=20)
    wikipedia_lang = models.CharField(max_length=10)
    wikipedia_title = models.CharField(max_length=255)

    def __str__(self):
        return self.wikipedia_title


class Campaign(models.Model):
    start_date = models.DateField(verbose_name=_("Pradžia"))
    end_date = models.DateField(verbose_name=_("Pabaiga"))
    is_active = models.BooleanField(verbose_name=_("Aktyvi"), default=False)

    class Meta:
        verbose_name = _("Akcija")
        verbose_name_plural = _("Akcijos")

    def __str__(self):
        return '{0:%Y-%m-%d} -- {1:%Y-%m-%d}'.format(self.start_date, self.end_date)


class Shift(models.Model):
    title = models.CharField(verbose_name=_("Pavadinimas"), max_length=255)
    visible = models.BooleanField(verbose_name=_("Rodoma"), default=True)

    class Meta:
        verbose_name = _("Pamaina")
        verbose_name_plural = _("Pamainos")

    def __str__(self):
        return self.title


class Organisation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False)
    places = models.ManyToManyField(Place, verbose_name=_("Vietos"))
    phone = models.CharField(verbose_name=_("Telefonas"), max_length=255)

    def __str__(self):
        return self.user.get_full_name()


class Volunteer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False)
    places = models.ManyToManyField(Place, verbose_name=_("Vietos"))
    phone = models.CharField(verbose_name=_("Telefonas"), max_length=255, blank=True)
    shift = models.ManyToManyField(Shift, verbose_name=_("Pamainos"))
    experience = models.IntegerField(verbose_name=_("Patirtis"), null=True, blank=True)
    campaigns = models.ManyToManyField(Campaign, through='VolunteerCampaign', verbose_name=_("Akcijos"), editable=False)

    class Meta:
        verbose_name = _("Savanoris")
        verbose_name_plural = _("Savanoriai")

    def __str__(self):
        return self.user.get_full_name()


class VolunteerCampaign(models.Model):
    """

    Properties:

        accepted (bool or None):
            None - Invitation was sent, but volunteer did not responded
            True - Volunteer accpeted inviation
            False - Volunteer refused inviation

    """
    volunteer = models.ForeignKey(Volunteer, verbose_name=_("Savanoris"), related_name='states')
    campaign = models.ForeignKey(Campaign, verbose_name=_("Akcija"))
    organisation = models.ForeignKey(Organisation, verbose_name=_("Organizacija"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Užsiregistravo"))
    accepted = models.NullBooleanField(verbose_name=_("Priimta"))
    removed = models.BooleanField(verbose_name=_("Pašalinta organizacijos"), default=False)

    class Meta:
        unique_together = ('volunteer', 'campaign', 'organisation')
