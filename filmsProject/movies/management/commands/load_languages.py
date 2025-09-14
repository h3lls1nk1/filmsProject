from django.core.management.base import BaseCommand
import json

from movies.models import Language

class Command (BaseCommand):
    help = 'Carga idiomas desde un JSON en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON de idiomas')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, encoding='utf-8') as f:
            languages = json.load(f)

        created_count = 0

        for lang in languages:
            obj, created = Language.objects.update_or_create(
                iso_code = lang['iso_code'],
                defaults={
                    'name': lang['name'],
                    'native_name': lang['native_name'],
                },
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} idiomas insertados/actualizados'))