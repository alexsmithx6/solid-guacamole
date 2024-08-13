from rest_framework import serializers
from spotify_history.models import *
from django.contrib.auth import get_user_model

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = album
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = song
        fields = '__all__'

class SongDetailSerializer(serializers.ModelSerializer):

    class ArtistSongSerializer(serializers.ModelSerializer):
        artist = ArtistSerializer()
        class Meta:
            model = artist_song
            fields = 'artist',

    album = AlbumSerializer()
    song_artists = serializers.SerializerMethodField()
    class Meta:
        model = song
        fields = '__all__'

    def get_song_artists(self, obj):
        # Fetch related artist_song entries for this song
        artist_songs = artist_song.objects.filter(song=obj)
        serializer = self.ArtistSongSerializer(artist_songs, many=True)
        return serializer.data
    
class ListenHistorySerializer(serializers.ModelSerializer):

    class AccountSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = 'uid',

    song = SongDetailSerializer()
    account = AccountSerializer()

    class Meta:
        model = listen_history
        fields = 'song', 'timestamp', 'account'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if 'song_artists' in representation:
    #         representation['song_artists'] = [
    #             {
    #                 'id': artist['artist']['id'],
    #                 'name': artist['artist']['name']
    #             }
    #             for artist in representation['song_artists']
    #         ]
    #     return representation
    