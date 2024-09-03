from loguru import logger
from rest_framework import generics, status
from rest_framework.views import APIView
from spotify_history.models import *
from spotify_history.serializers import *
from users.models import app, token
from django.contrib.auth import get_user_model
from dateutil.parser import parse

from django.conf import settings
# ExecuteDataload view specific imports
from spotify_history.functions import internal_dataload_process
from rest_framework.response import Response

# Artist serializers
class ArtistListView(generics.ListAPIView):
    queryset = artist.objects.all()
    serializer_class = ArtistSerializer

class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = artist.objects.all()
    serializer_class = ArtistSerializer

# Album serializers
class AlbumListView(generics.ListAPIView):
    queryset = album.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = album.objects.all()
    serializer_class = AlbumSerializer

# Song serializers
class SongListView(generics.ListAPIView):
    queryset = song.objects.all()
    serializer_class = SongSerializer

class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = song.objects.all()
    serializer_class = SongDetailSerializer
    
class History(APIView):
    """
    Get Spotify listening history OR execute dataload process
    """

    # permission_classes = [IsAuthenticated]  # Require authentication

    def get_view_description(self, html=False):
        return f'Get Spotify listening history OR execute dataload process'
    
    def get(self, request, uid, *args, **kwargs):
        # Retrieve user object
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
            
        queryset = listen_history.objects.filter(account=account_obj).order_by('-timestamp')
        # Get the 'n' parameter from the request query parameters
        n = self.request.query_params.get('n', None)
        start_time = self.request.query_params.get('start_time', None)

        # Check start_time parameter (optional) + apply to queryset if used
        if start_time is not None:
            try:
                start_time = parse(start_time)
                # listen_history.timestamp GREATER THAN input start_time:
                queryset = queryset.filter(timestamp__gt=start_time)
            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'Invalid type for start_time'}
                )

        # Check n parameter (optional) + apply to queryset if used
        if n is not None:
            try:
                n = int(n)
            # Exception due to typecast error
            except Exception:
                # Bad request due to parameter
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'Invalid type for n'}
                )

            if n > 0:
                queryset = queryset[:n]
            else:
                # Bad request due to parameter n < 1
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'Invalid value for n'}
                )

        serializer = ListenHistorySerializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
    
    def post(self, request, uid, *args, **kwargs):
        try:
            internal_dataload_process(uid, 50)
            return Response(status=status.HTTP_200_OK)
        # User not found
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Token not found i.e. user has not authenticated against Spotify API
        except token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Other exception types
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)