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
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity;
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

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

def get_artist_info(session_id, artist_uri):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    artist_info = spotify.artist(artist_uri)

    return artist_info

def get_features(session_id, track_id):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    track_features = spotify.audio_features(track_id)

    return track_features

def extract_data(session_id,playlist_df, playlist_id):
    songs = get_playlist_songs(session_id, playlist_id)
    for track in songs['items']:
        try:
            track_id = track["track"]["id"]
            track_name = track["track"]["name"]
            track_pop = track["track"]["popularity"]

            # Main Artist infos
            artist_uri = track["track"]["artists"][0]["uri"]
            artist_name = track["track"]["artists"][0]["name"]
            artist_info = get_artist_info(artist_uri)
            artist_pop = artist_info["popularity"]
            genres = artist_info['genres']

            features = get_features(session_id,track_id)
            for feature in features:
                danceability = feature["danceability"]
                energy = feature["energy"]
                key = feature["key"]
                loudness = feature["loudness"]
                mode = feature["mode"]
                speechiness  = feature["speechiness"]
                acousticness = feature["acousticness"]
                instrumentalness = feature["instrumentalness"]
                liveness = feature["liveness"]
                valence = feature["valence"]  # A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. 
                tempo = feature["tempo"]

            series = pd.Series([track_id, track_name, track_pop ,artist_name, artist_pop, genres, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo])
            playlistDF = pd.concat([playlistDF, series],axis = 1, ignore_index = True)

        except:
            continue
    
    playlistDF = playlistDF.transpose()
    playlistDF.columns = ['track_id', 'track_name', 'track_pop', 'artist_name', 'artist_pop', 'genres', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    playlistDF = playlistDF.astype(dtype = {'track_id' : str,
                                        'track_name' : str, 
                                        'track_pop' : int, 
                                        'artist_name' : str, 
                                        'artist_pop': float, 
                                        'genres' : object, 
                                        'danceability' : float, 
                                        'energy' : float, 
                                        'key' : int, 
                                        'loudness' : float, 
                                        'mode' : float, 
                                        'speechiness' : float, 
                                        'acousticness' : float, 
                                        'instrumentalness' : float, 
                                        'liveness' : float, 
                                        'valence' : float, 
                                        'tempo' : float })
                                        
    return playlistDF
