import funcy
import factory

from factory.django import DjangoModelFactory

from savanoriai.core.models import Place, Shift


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
