# Django/Third-Party dependencies
from django.db import connection
from django.contrib.auth import get_user_model
from users.models import app, token
# Base imports
import requests, json
from urllib.parse import urljoin
# Project imports
from django.conf import settings
from utils.exception_handlers import CLIENT_ERRORS, SERVER_ERRORS, ClientError, ServerError
from users.utils.spotify_oauth import SpotifyOAuth2Session
# Logging
from loguru import logger

SPOTIFY_API_RECENTLY_PLAYED_TRACKS_URI = urljoin(settings.SPOTIFY_API_BASE_URL, settings.SPOTIFY_API_RECENTLY_PLAYED_TRACKS_ENDPOINT)

def execute_process_spotify_api_response(uid : int, data : dict) -> None:
    # TODO: make this procedure execution safer
    user_pk = get_user_model().objects.get(uid=uid).id
    with connection.cursor() as cursor:
        cursor.execute("""
            CALL public.process_spotify_api_response(%s, %s)
        """, [user_pk, json.dumps(data).replace('\'', '\'\'')])

def internal_dataload_process(uid: int, num_items: int):

    logger.debug('Retrieving Spotify provider social account + API token')
    # Retrieve user object
    account_obj = get_user_model().objects.get(
        uid=uid, 
        app=app.get_or_create_spotify()
    )
    session = SpotifyOAuth2Session(account_obj)

    logger.debug(f'Sending request to Spotify API for user listen history {num_items=}')
    try:
        # Send request to API
        response = session.get(
            url=SPOTIFY_API_RECENTLY_PLAYED_TRACKS_URI,
            params={
                'limit': str(num_items)
            }
        )
        # Raise for status in event of an error
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        logger.exception(f'Request has failed with exception: {str(e)}')

        # Check if a response from the API was successfully receieved
        if 'application/json' in response.headers.get('Content-Type', ''):
            logger.debug(f'Error response: {response.json()}')

        # Re-throw exception
        raise

    logger.debug('Executing dataload procedure for Spotify API response')
    execute_process_spotify_api_response(uid, data)