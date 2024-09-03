from django.urls import path
from users.views import spotify_oauth2_login_view, spotify_oauth2_callback_view, Account

urlpatterns = [
    path('spotify/auth_uri/', spotify_oauth2_login_view, name='spotify_login'),
    path('spotify/login/callback/', spotify_oauth2_callback_view, name='spotify_login_callback'),
    path('<str:uid>/', Account.as_view(), name='account'),
]