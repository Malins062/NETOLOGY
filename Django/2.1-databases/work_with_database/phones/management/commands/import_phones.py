import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            try:
                p = Phone(**phone,
                          slug=phone['name'].replace(' ', '-'))
                p.save()
            except Exception as err:
                print(f'Ошибка добавления данных: {err}')
