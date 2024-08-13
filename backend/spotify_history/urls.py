from django.urls import path

from spotify_history.views import *

urlpatterns = [
    # Artist endpoints
    path('artist/', ArtistListView.as_view(), name='artist_list'),
    path('artist/<str:pk>/', ArtistDetailView.as_view(), name='artist_detail'),
    # Album endpoints
    path('album/', AlbumListView.as_view(), name='album_list'),
    path('album/<str:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    # Song endpoints
    path('song/', SongListView.as_view(), name='song_list'),
    path('song/<str:pk>/', SongDetailView.as_view(), name='song_detail'),
    # GET listen history + POST dataload process endpoint
    path('<str:uid>/', History.as_view(), name='history'),
]