from django.urls import path

from .views import *

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('playlists', GetUserPlaylists.as_view()),
    path('pl', GetPlaylist.as_view(), name='playlists'),
    path('songs', GetPlaylistSongs.as_view()),
]

