from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Deletes either a single table or the whole database'

    def add_arguments(self, parser):
        parser.add_argument('--table', type=str, help='Name of the table to delete')
        parser.add_argument('--all', action='store_true', help='Delete the whole database')

    def handle(self, *args, **options):
        table_name = options.get('table')
        delete_all = options.get('all')

        if table_name and not delete_all:
            self.delete_table(table_name)
        elif delete_all and not table_name:
            self.delete_database()
        else:
            self.stderr.write(self.style.ERROR('Please specify either --table or --all'))

    def delete_table(self, table_name):
        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        self.stdout.write(self.style.SUCCESS(f'Table "{table_name}" deleted successfully'))

    def delete_database(self):
        with connection.cursor() as cursor:
            table_names = connection.introspection.table_names()

            # Disable foreign key checks to avoid errors when dropping tables
            cursor.execute('PRAGMA foreign_keys=OFF')

            # Drop each table
            for table_name in table_names:
                cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

            # Enable foreign key checks
            cursor.execute('PRAGMA foreign_keys=ON')

        self.stdout.write(self.style.SUCCESS('All tables deleted successfully'))
