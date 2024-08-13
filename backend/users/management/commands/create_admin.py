from django.core.management.base import BaseCommand
from users.models import account
import os
from utils.function_decorators import try_catch_decorator

class Command(BaseCommand):
    help = 'Run project unit tests'

    def handle(self, *args, **options):

        @try_catch_decorator
        def function(*args, **options):
            # Credentials from environment variables
            username = os.environ['DJANGO_SUPERUSER_USERNAME']
            email = os.environ['DJANGO_SUPERUSER_EMAIL']
            password = os.environ['DJANGO_SUPERUSER_PASSWORD']
            # Create if not exists
            if not account.objects.filter(username=username).exists():
                account.objects.create_superuser(username, email, password)

        # Allowed to fail with suppression
        function(*args, **options)