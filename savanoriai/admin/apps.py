from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SavanoriaiAdminConfig(AppConfig):
    name = 'savanoriai.admin'
    label = 'savanoriaiadmin'
    verbose_name = _("Savanorių duomenų bazės administravimas")
