from django.apps import apps
from django.conf import settings


def update_default_site(app_config, verbosity=2, **kwargs):  # pylint: disable=unused-argument
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get_current()

    if site.domain == 'example.com':
        site.domain = settings.SERVER_NAME
        site.name = 'savanoriai.maistobankas.lt'
        site.save()
