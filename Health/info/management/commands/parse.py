from django.core.management import BaseCommand
from info.parser import parse_document
from info.services import update_database
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = parse_document()
        self.stdout.write(self.style.SUCCESS('Document was successfully parsed'))
        self.stdout.write(self.style.SUCCESS(f'Updating database'))
        update_database(data)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
