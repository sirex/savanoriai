from savanoriai.settings.base import *  # noqa

DEBUG = False

DEFAULT_FROM_EMAIL = 'info@maistobankas.lt'

ALLOWED_HOSTS = [
    'savanoriai.maistobankas.lt',
]

DATABASES = {
    'default': env.db(default='psql:///savanoriai'),
}
