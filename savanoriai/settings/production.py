from savanoriai.settings.base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [
    'savanoriai.maistobankas.lt',
]

DATABASES = {
    'default': env.db(default='psql:///savanoriai'),
}
