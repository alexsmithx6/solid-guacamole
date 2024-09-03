# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import artist, album, artist_album, song, artist_song, listen_history


@admin.register(artist)
class artistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(album)
class albumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'release_date', 'len', 'art_url')
    list_filter = ('release_date',)
    search_fields = ('name',)


@admin.register(artist_album)
class artist_albumAdmin(admin.ModelAdmin):
    list_display = ('id', 'artist', 'album')
    list_filter = ('artist', 'album')


@admin.register(song)
class songAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'name', 'index', 'duration')
    search_fields = ('name',)


@admin.register(artist_song)
class artist_songAdmin(admin.ModelAdmin):
    list_display = ('id', 'artist', 'song')


@admin.register(listen_history)
class listen_historyAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'song', 'timestamp')
    list_filter = ('timestamp',)
