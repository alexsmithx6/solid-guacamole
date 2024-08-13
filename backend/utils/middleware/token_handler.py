# # Django/Third-Party dependencies
# from django.db import connection
# from django.contrib.auth import get_user_model
# from allauth.socialaccount.models import SocialToken, SocialAccount
# from allauth.socialaccount.providers.spotify.views import SpotifyOAuth2Adapter
# # Base imports
# import requests, json
# from urllib.parse import urljoin
# # Project imports
# from django.conf import settings
# from utils.exception_handlers import CLIENT_ERRORS, SERVER_ERRORS, ClientError, ServerError
# from app.backend.auth.utils.spotify_refresh_token import refresh_user_token
# # Logging
# from loguru import logger

# from django.utils.deprecation import MiddlewareMixin
# class TokenMiddleware(MiddlewareMixin):    
#     def process_request(self, request):

#         logger.debug('Middleware refreshing Spotify API token')
#         try:
#             if request.user.id:
#                 # Retrieve user object
#                 user = get_user_model().objects.get(id=request.user.id)
#                 # Retrieve social account object
#                 social_account = SocialAccount.objects.get(user=user, provider='spotify')
#                 # Retrieve social account token object - bearer token for Spotify API
#                 token = SocialToken.objects.get(account=social_account)
#                 # Call refresh user token routine
#                 refresh_user_token(token)

#         except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist) as e:
#             raise ClientError(e, 404)

#         except Exception as e:
#             raise ServerError(e)

#         return None