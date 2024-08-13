from datetime import datetime
from typing import Any
# Project dependencies
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
# Logging
from loguru import logger

from oauthlib.oauth2 import Client
from requests_oauthlib import OAuth2Session

# class user(AbstractUser):
#     pass

# Create your models here.
class app(models.Model):
    name = models.CharField(unique=True, null=False, blank=False)

    @classmethod
    def get_or_create_spotify(cls):
        # Moved inside a try-catch so that if there are database issues we won't fail here.
        try:
            return cls.objects.get_or_create(name=settings.SPOTIFY_APP_NAME)[0]
        except Exception:
            return None
    
class account(AbstractUser):

    app = models.ForeignKey(app, null=False, blank=False, on_delete=models.CASCADE, default=app.get_or_create_spotify)
    uid = models.CharField(unique=True, max_length=32, null=False, blank=False)

    # Define a single name field
    name = models.CharField(max_length=255, blank=True, null=True, default='')

    def save(self, *args, **kwargs):
        # Automatically combine first_name and last_name if not already declared
        if self.name == '':
            self.name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Change this to something unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self) -> str:
        return f'{self.name} - {self.uid}'

    # class Meta:
    #     unique_together = ('app', 'uid')

class token(models.Model):

    account = models.OneToOneField(account, null=False, blank=False, on_delete=models.CASCADE)

    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.account} - token'

# def get_or_create_user(app_name: str, account_uid: str):

#     app_obj, created = app.objects.get_or_create(name=app_name)
#     if created:
#         logger.info(f'Created app entry in database: {app_obj}')
    
#     account_obj, created = account.objects.get_or_create(app=app_obj, uid=account_uid)
#     if created:
#         logger.info(f'Created account entry in database: {account_obj}')

#     token_obj, created = token.objects.get_or_create()