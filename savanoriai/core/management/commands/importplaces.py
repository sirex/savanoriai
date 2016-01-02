import csv
import codecs
import urllib.request
import tqdm

from django.db import transaction
from django.core.management.base import BaseCommand

from savanoriai.core.models import Place


class Command(BaseCommand):
    help = 'Import places data'

    def handle(self, *args, **options):
        url = 'http://atviriduomenys.lt/data/osm/places.csv'
        with urllib.request.urlopen(url) as f, transaction.atomic():
            reader = codecs.getreader('utf-8')
            rows = csv.DictReader(reader(f))
            for row in tqdm.tqdm(rows):
                place = Place(
                    county=row['admin_level_4'],
                    municipality=row['admin_level_5'],
                    eldership=row['admin_level_5'],
                    lat=row['lat'],
                    lon=row['lon'],
                    osm_id=row['osm_id'],
                    place=row['place'],
                    population=int(row['population']) if row['population'] else None,
                    type=row['type'],
                    wikipedia_lang=row['wikipedia_lang'],
                    wikipedia_title=row['wikipedia_title'],
                )
                place.save()
