# Project dependencies
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(null=False, max_length=64)

    def __str__(self):
        return self.name

class album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(null=False, max_length=64)
    release_date = models.DateField(null=False)
    len = models.IntegerField(null=False)
    art_url = models.CharField(null=False, max_length=128)

    def __str__(self):
        return self.name

class artist_album(models.Model):
    artist = models.ForeignKey(artist, on_delete=models.CASCADE)
    album = models.ForeignKey(album, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('artist', 'album'),)
    def __str__(self):
        return f'{self.artist} - {self.album}'
    
class song(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    album = models.ForeignKey(album, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=64)
    index = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class artist_song(models.Model):
    artist = models.ForeignKey(artist, on_delete=models.CASCADE)
    song = models.ForeignKey(song, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('artist', 'song'),)
    def __str__(self):
        return f'{self.artist.name} - {self.song.name}'

class listen_history(models.Model):
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    song = models.ForeignKey(song, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        unique_together = ('account', 'timestamp')
    def __str__(self):
        return f'{self.account} listened to {self.song} at {self.timestamp}'