# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import app, account, token


@admin.register(app)
class appAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(account)
class accountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'app',
        'uid',
        'name',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'app',
    )
    raw_id_fields = ('groups', 'user_permissions')
    search_fields = ('name',)


@admin.register(token)
class tokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'access_token',
        'refresh_token',
        'expires_at',
    )
    list_filter = ('account',)
