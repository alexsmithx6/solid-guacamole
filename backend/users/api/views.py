from users.api.serializers import *
from users.models import app, account, token
from django.contrib.auth import get_user_model
from dateutil.parser import parse
from django.shortcuts import get_object_or_404

from django.http import Http404

from urllib.parse import urljoin
from django.conf import settings

# REST Framework dependencies
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

import requests

from requests_oauthlib import OAuth2Session



# class AccountView(generics.RetrieveAPIView):
#     serializer_class = AcccountSerializer

#     def get(self, request, *args, **kwargs):

#         try:
#             account_obj = get_object_or_404(account, app=app.get_or_create_spotify(), uid=kwargs['uid'])
#             token_obj = get_object_or_404(token, account=account_obj)
#         except Http404:
#             return Response(status=HTTP_404_NOT_FOUND)

#         # OAuth2 session (no authorization response)
#         session = OAuth2Session(
#             settings.SPOTIFY_API_CLIENT_ID,
#             redirect_uri=redirect_uri,
#             scope=settings.SPOTIFY_API_SCOPE,
#         )


#         try:
#             requests.get(SPOTIFY_API_ME_URI).json()
#         except Exception as exitMessage:

#         SPOTIFY_API_ME_URI).json()

#         return Response(status=HTTP_200_OK, data=data)
