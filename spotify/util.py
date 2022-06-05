from datetime import timedelta
import json
from traceback import print_tb
from .models import SpofityToken
from django.utils import timezone
import os
from requests import post, put, get
from datetime import timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BASE_URL = 	"https://api.spotify.com/v1/"

def get_user_tokens(session_id):
    user_tokens = SpofityToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, refresh_token, expires_in):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])

    else:
        tokens = SpofityToken(user=session_id, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)

        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expire_date = tokens.expires_in
        if expire_date <= timezone.now():
            refresh_spotify_token(session_id)
            return True
    return False

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, access_token, token_type, refresh_token,expires_in)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + tokens.access_token
    }

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint , {}, headers=headers)

    try:
        return response.json()
    except:
        return {'Error': 'We are having issues with request'}

def get_playlist(session_id):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    playlists = spotify.current_user_playlists()

    #print(playlists["items"][0]["id"])
    #print(playlists["total"])

    return playlists

def get_playlist_songs(session_id, playlist_id):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    songs = spotify.playlist_tracks(playlist_id=playlist_id)

    return songs

def get_current_user_id(session_id):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    user_id = spotify.current_user()

    return user_id['id']


