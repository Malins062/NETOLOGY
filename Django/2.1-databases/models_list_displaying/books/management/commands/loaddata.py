import json

from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            type=str,
            dest='args'
        )

    def handle(self, *args, **options):
        with open(''.join(args), 'r', encoding='utf-8') as file:
            books = json.load(file)

        for book in books:
            try:
                Book.objects.create(**book['fields'])
            except Exception as err:
                print(f'Ошибка добавления данных: {err}')
