import funcy
import factory

from django.conf import settings

from factory.django import DjangoModelFactory

from allauth.account.models import EmailAddress
from savanoriai.core.models import Place, Shift, Organisation, Volunteer


class PlaceFactory(DjangoModelFactory):
    osm_id = factory.Sequence(funcy.identity)
    county = 'Vilniaus apskritis'
    municipality = 'Vilniaus miesto savivaldybė'
    eldership = 'Senamiestis'
    place = 'Senamiestis'
    type = 'suburb'
    population = 9999
    wikipedia_lang = 'lt'
    wikipedia_title = 'Senamiestis'
    lat = 25.2884035
    lon = 54.6818728

    class Meta:
        model = Place
        django_get_or_create = ('wikipedia_title',)


shifts = [
    'Pirmadienis (14:45-18:00)',
    'Pirmadienis (17:45-21:15)',
    'Šeštadienis (09:45-13:30)',
    'Šeštadienis (13:15-17:00)',
    'Šeštadienis (16:45-20:30)',
]


class ShiftFactory(DjangoModelFactory):
    title = factory.Iterator(shifts, cycle=False)
    visible = True

    class Meta:
        model = Shift
        django_get_or_create = ('title',)


class EmailAddressFactory(DjangoModelFactory):
    email = factory.SelfAttribute('user.email')
    verified = True
    primary = True

    class Meta:
        model = EmailAddress
        django_get_or_create = ('email',)


class UserFactory(DjangoModelFactory):
    first_name = 'Vardenis'
    last_name = 'Pavardenis'
    email = 'text@example.com'
    is_active = True
    emailaddress = factory.RelatedFactory(EmailAddressFactory, 'user')

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)


class OrganisationFactory(DjangoModelFactory):
    user = factory.SubFactory(
        UserFactory,
        username='org',
        email='org@example.com',
        first_name='Organizacija',
        last_name='',
    )
    phone = '111111111'

    class Meta:
        model = Organisation

    @factory.post_generation
    def places(self, create, extracted, **kwargs):
        if create:
            self.places = extracted or [PlaceFactory()]


class VolunteerFactory(DjangoModelFactory):
    user = factory.SubFactory(
        UserFactory,
        username='volunteer',
        email='volunteer@example.com',
        first_name='Volunteer',
        last_name='Volunteerer',
    )
    phone = '111111112'
    place = factory.SubFactory(PlaceFactory)
    experience = 1

    class Meta:
        model = Volunteer

    @factory.post_generation
    def shift(self, create, extracted, **kwargs):
        if create:
            self.shift = extracted or [ShiftFactory(title='Pirmadienis (14:45-18:00)')]
