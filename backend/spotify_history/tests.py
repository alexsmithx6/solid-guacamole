from django.test import TestCase

from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from spotify_history.models import *

class SpotifyDatabaseTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.artist = artist.objects.create(**{
            "id": "4qrHkx5cgWIslciLXUMrYw",
            "name": "Knocked Loose"
        })

        self.artist_outer = artist.objects.create(**{
            "id": "5mlbvTfWUOfDrUIK6dkNzv",
            "name": "Poppy"
        })

        self.album = album.objects.create(**{
            "id": "2sLBMdUF5HYNB0voqWs4K3",
            "name": "You Won''t Go Before You''re Supposed To",
            "release_date": "2024-05-10",
            "len": 10,
            "art_url": "https://i.scdn.co/image/ab67616d0000b273e5f143a6fbd201f53f38e86d"
        })

        self.song = song.objects.create(**{
            "id": "6PXYOVPBzO3xojFhQAvmde",
            "name": "Suffocate (feat. Poppy)",
            "index": 3,
            "duration": 164695,
            "album_id": "2sLBMdUF5HYNB0voqWs4K3"
        })

        self.artist_album = artist_album.objects.create(**{
            "id": "1",
            "artist_id": "4qrHkx5cgWIslciLXUMrYw",
            "album_id": "2sLBMdUF5HYNB0voqWs4K3",  
        })

        self.artist_song = artist_song.objects.create(**{
            "id": "1",
            "artist_id": "4qrHkx5cgWIslciLXUMrYw",
            "song_id": "6PXYOVPBzO3xojFhQAvmde",  
        })

        self.artist_song = artist_song.objects.create(**{
            "id": "2",
            "artist_id": "5mlbvTfWUOfDrUIK6dkNzv",
            "song_id": "6PXYOVPBzO3xojFhQAvmde",  
        })

    def test_ArtistDetailView(self):

        # Happy path
        response = self.client.get(reverse('artist_detail', args=[self.artist.id]), follow=True)
        # Assert 200 + correct JSON response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), model_to_dict(self.artist))

        # Unhappy path
        response = self.client.get(reverse('artist_detail', args=['bad_id']), follow=True)
        # Assert 404 + error JSON response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "No artist matches the given query."})

    def test_AlbumDetailView(self):

        # Happy path
        response = self.client.get(reverse('album_detail', args=[self.album.id]), follow=True)
        # Assert 200 + correct JSON response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), model_to_dict(self.album))

        # Unhappy path
        response = self.client.get(reverse('album_detail', args=['bad_id']), follow=True)
        # Assert 404 + error JSON response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "No album matches the given query."})

    def test_SongDetailView(self):
        
        # Happy path
        response = self.client.get(reverse('song_detail', args=[self.song.id]), follow=True)
        # Assert 200 + correct JSON response
        expected_data = {
            "id": "6PXYOVPBzO3xojFhQAvmde",
            "album": {
                "id": "2sLBMdUF5HYNB0voqWs4K3",
                "name": "You Won''t Go Before You''re Supposed To",
                "release_date": "2024-05-10",
                "len": 10,
                "art_url": "https://i.scdn.co/image/ab67616d0000b273e5f143a6fbd201f53f38e86d"
            },
            "song_artists": [
                {
                    "artist": {
                        "id": "4qrHkx5cgWIslciLXUMrYw",
                        "name": "Knocked Loose"
                    }
                },
                {
                    "artist": {
                        "id": "5mlbvTfWUOfDrUIK6dkNzv",
                        "name": "Poppy"
                    }
                }
            ],
            "name": "Suffocate (feat. Poppy)",
            "index": 3,
            "duration": 164695
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_data)

        # Unhappy path
        response = self.client.get(reverse('song_detail', args=['bad_id']), follow=True)
        # Assert 404 + error JSON response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "No song matches the given query."})

