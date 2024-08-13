from django.core.management.base import BaseCommand
from tests import run_tests
class Command(BaseCommand):
    help = 'Run project unit tests'
    def handle(self, *args, **options):
        run_tests()        
    