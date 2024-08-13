from django.core.management.base import BaseCommand
from django.db import connection

from spotify_history.migrations.plpgsql import load_sql_from_file

class Command(BaseCommand):
    help = 'Apply database function migrations, with rollback capability'

    sql_commands = [
        {
            'up': load_sql_from_file('add_item_to_db'),
            'down': "DROP PROCEDURE IF EXISTS public.add_item_to_db;"
        },
        {
            'up': load_sql_from_file('process_spotify_api_response'),
            'down': "DROP PROCEDURE IF EXISTS public.process_spotify_api_response;"
        }
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--reverse',
            action='store_true',
            help='Reverse the SQL migration',
        )

    def handle(self, *args, **options):
        if options['reverse']:
            self.reverse()
        else:
            self.forward()        
    
    def reverse(self):
        self.stdout.write(self.style.MIGRATE_LABEL('Reversing function migrations'))
        self.__execute_commands(method='down')
        self.stdout.write(self.style.SUCCESS('Functions removed from database successfully'))

    def forward(self):
        self.stdout.write(self.style.MIGRATE_LABEL('Applying function migrations'))
        self.__execute_commands(method='up')
        self.stdout.write(self.style.SUCCESS('Functions migrated to database successfully'))

    def __execute_commands(self, method):
        # Apply the SQL commands
        with connection.cursor() as cursor:
            for command in self.sql_commands:
                cursor.execute(command[method])