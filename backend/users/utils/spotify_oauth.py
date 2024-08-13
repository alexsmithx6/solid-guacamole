# Project dependencies

# Base imports
from datetime import datetime
# Logging
from loguru import logger
from urllib.parse import urljoin
from django.conf import settings
from requests_oauthlib import OAuth2Session
from users.models import app, account, token

SPOTIFY_API_ME_URI = urljoin(
    settings.SPOTIFY_API_BASE_URL, 
    settings.SPOTIFY_API_USER_PROFILE_ENDPOINT
)

class SpotifyOAuth2Session(OAuth2Session):

    def __init__(self, account_obj=None, *args, **kwargs):

        if account_obj is not None:
            self.account_obj = account_obj
            self.token_obj, created = token.objects.get_or_create(
                account = self.account_obj,
            )

        else:
            self.account_obj = None
            self.token_obj = token()
            created = False

        self.user_data = {}

        if not created:
            token_dict = {
                'access_token': self.token_obj.access_token,
                'token_type': 'Bearer',
                'refresh_token': self.token_obj.refresh_token,
                'expires_at': self.token_obj.expires_at
            }

        else:
            token_dict = None

        super().__init__(
            client_id=settings.SPOTIFY_API_CLIENT_ID, 
            token=token_dict, 
            auto_refresh_kwargs={
                'client_id': settings.SPOTIFY_API_CLIENT_ID, 
                'client_secret': settings.SPOTIFY_API_CLIENT_SECRET
            },
            auto_refresh_url=settings.SPOTIFY_API_TOKEN_URL,
            token_updater=self.token_updater,
            *args, 
            **kwargs  
        )
        
    def token_updater(self, token_dict):

        # Update user account as needed
        self.account_updater()

        logger.info(f'Updating token for user {self.account_obj}')
        # Save or get existing token
        self.token_obj, _ = token.objects.get_or_create(
            account = self.account_obj,
        )
        self.token_obj.access_token = str(token_dict['access_token'])
        self.token_obj.refresh_token = str(token_dict['refresh_token'])
        self.token_obj.expires_at = datetime.now().timestamp() + int(token_dict['expires_in'])
        # Save token after data modifications
        self.token_obj.save()

    def account_updater(self):

        # Send API request after successful authentication against Spotify API
        resp = self.get(SPOTIFY_API_ME_URI)
        resp.raise_for_status()
        self.user_data = resp.json()

        logger.debug(f'Retrieving user data from Spotify API response')
        # Save or get existing user
        self.account_obj, created = account.objects.get_or_create(
            uid = self.user_data['id'],
            app = app.get_or_create_spotify()
        )
        self.account_obj.email = self.user_data['email']
        self.account_obj.name = self.user_data['display_name']
        # Save user after data modifications
        self.account_obj.save()
        if created:
            logger.info(f'Created new user: {self.account_obj}')
        else:
            logger.debug(f'Existing user authenticated: {self.account_obj}')

        # Also updating token object's assigned account
        self.token_obj.account = self.account_obj

def spotify_auth(redirect_uri: str):

    # OAuth2 session (no authorization response)
    session = SpotifyOAuth2Session(
        redirect_uri=redirect_uri,
        scope=settings.SPOTIFY_API_SCOPE,
    )

    # Generate authorization URL to send user to
    authorization_url, _ = session.authorization_url(
        settings.SPOTIFY_API_AUTH_URL, 
        access_type="offline", 
        prompt="select_account")

    return authorization_url

def spotify_callback(redirect_uri: str, auth_uri: str):

    # OAuth2 session (authorization response provided)
    session = SpotifyOAuth2Session(
        redirect_uri=redirect_uri
    )

    # Retrieving token for Spotify API
    session.fetch_token(
        token_url=settings.SPOTIFY_API_TOKEN_URL,
        client_secret=settings.SPOTIFY_API_CLIENT_SECRET,
        authorization_response=auth_uri,
    )

    # TODO - update SpotifyOAuth2Session.fetch_token such that this is called automatically inside the function?
    session.token_updater(session.token)

    logger.info(f'Successfully authenticated for user: {session.account_obj}')
    return session.user_data

