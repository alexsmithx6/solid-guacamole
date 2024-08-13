from django.urls import path
from users.views.spotify import spotify_oauth2_login_view, spotify_oauth2_callback_view

urlpatterns = [
    path('spotify/login', spotify_oauth2_login_view, name='spotify_login'),
    path('spotify/login/callback', spotify_oauth2_callback_view, name='spotify_login_callback'),
]