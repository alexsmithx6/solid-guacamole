# Django dependencies
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
# REST Framework dependencies
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
# Other dependencies
from loguru import logger
# Project dependencies
from users.models import app
from users.utils.spotify_oauth import SpotifyOAuth2Session, spotify_auth, spotify_callback

class SpotifyOAuth2LoginView(APIView):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("spotify_login_callback"))
        return Response(status=HTTP_200_OK, data = {'auth_uri': spotify_auth(redirect_uri)})
        # return redirect(spotify_auth(redirect_uri))
    
spotify_oauth2_login_view = SpotifyOAuth2LoginView.as_view()

class SpotifyOAuth2LoginCallbackView(APIView):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("spotify_login_callback"))
        auth_uri = request.build_absolute_uri()
        user_data = spotify_callback(redirect_uri, auth_uri)
        return Response(status=HTTP_200_OK, data=user_data)

# class SpotifyOAuth2LoginCallbackView(APIView):
#     def get(self, request):
#         redirect_uri = request.build_absolute_uri(reverse("spotify_login_callback"))
#         auth_uri = request.build_absolute_uri()
#         user_data = spotify_callback(redirect_uri, auth_uri)
#         return Response(status=HTTP_200_OK, data=user_data)
    
spotify_oauth2_callback_view = SpotifyOAuth2LoginCallbackView.as_view()

class Account(APIView):
    """
    View account details
    """

    # permission_classes = [IsAuthenticated]  # Require authentication

    def get_view_description(self, html=False):
        return f'View account details'
    
    def get(self, request, uid, *args, **kwargs):

        # Retrieve user object + user details via Oauth2 session
        try:
            account_obj = get_user_model().objects.get(
                uid=uid, 
                app=app.get_or_create_spotify()
            )
        # User not found
        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'error': f'User {uid} not found'}
            )
        # Other exception types
        except Exception:
            logger.exception(f'Exception encountered')
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'error': f'Internal server error'}
            )

        session = SpotifyOAuth2Session(account_obj=account_obj)

        return Response(
            status=status.HTTP_200_OK,
            data=session.get_user_details()
        )