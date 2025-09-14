from django.core.management.base import BaseCommand
import json

from movies.models import Country

class Command (BaseCommand):
    help = 'Carga países desde un JSON en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON de países')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, encoding='utf-8') as f:
            countries = json.load(f)

        created_count = 0

        for country_data in countries:
            obj, created = Country.objects.update_or_create(
                iso_code = country_data['iso_code'],
                defaults={
                    'name': country_data['name'],
                    'flag_emoji': country_data['flag'],
                },
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} países insertados/actualizados'))