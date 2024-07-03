from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Truncates either a single table or the whole database'

    def add_arguments(self, parser):
        parser.add_argument('--table', type=str, help='Name of the table to truncate')
        parser.add_argument('--all', action='store_true', help='Truncate the whole database')

    def handle(self, *args, **options):
        table_name = options.get('table')
        truncate_all = options.get('all')

        if table_name and not truncate_all:
            self.truncate_table(table_name)
        elif truncate_all and not table_name:
            self.truncate_database()
        else:
            self.stderr.write(self.style.ERROR('Please specify either --table or --all'))

    def truncate_table(self, table_name):
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute(f'DELETE FROM {table_name}')
            else:
                cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
        self.stdout.write(self.style.SUCCESS(f'Table "{table_name}" truncated successfully'))

    def truncate_database(self):
        # Standard metadata tables to exclude
        metadata_tables = [
            'auth_group','auth_group_permissions','auth_permission','auth_user','auth_user_groups','auth_user_user_permissions',
            'django_migrations', 'django_content_type', 'django_admin_log',
            'django_session', 'django_site'
        ]

        # Add the user table to the exclusion list
        user_table = settings.AUTH_USER_MODEL.replace('.', '_').lower()
        metadata_tables.append(user_table)

        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute('PRAGMA foreign_keys=OFF')
                for table_name in connection.introspection.table_names():
                    if table_name not in metadata_tables:
                        cursor.execute(f'DELETE FROM {table_name}')
                cursor.execute('PRAGMA foreign_keys=ON')
            else:
                for table_name in connection.introspection.table_names():
                    if table_name not in metadata_tables:
                        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
        self.stdout.write(self.style.SUCCESS('All non-metadata tables truncated successfully'))


