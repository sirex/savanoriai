from savanoriai.settings.base import *  # noqa

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# django-debug-toolbar
# http://django-debug-toolbar.readthedocs.org/en/1.4/installation.html

INSTALLED_APPS += [
    'debug_toolbar',
]
