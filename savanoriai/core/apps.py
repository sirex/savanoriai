from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from savanoriai.core.management import update_default_site


class SavanoriaiCoreConfig(AppConfig):
    name = 'savanoriai.core'
    verbose_name = _("Savanorių duomenų bazė")

    def ready(self):
        post_migrate.connect(update_default_site, sender=self)
