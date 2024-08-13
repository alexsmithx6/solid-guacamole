# Django dependencies
from django.shortcuts import redirect
from django.urls import reverse
# REST Framework dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
# Project dependencies
from users.utils.spotify_oauth import spotify_auth, spotify_callback

class SpotifyOAuth2LoginView(APIView):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("spotify_login_callback"))
        return redirect(spotify_auth(redirect_uri))
    
spotify_oauth2_login_view = SpotifyOAuth2LoginView.as_view()
    
class SpotifyOAuth2LoginCallbackView(APIView):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("spotify_login_callback"))
        auth_uri = request.build_absolute_uri()
        user_data = spotify_callback(redirect_uri, auth_uri)
        return Response(status=HTTP_200_OK, data=user_data)
    
spotify_oauth2_callback_view = SpotifyOAuth2LoginCallbackView.as_view()
