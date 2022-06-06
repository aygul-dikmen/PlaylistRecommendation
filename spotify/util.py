from datetime import timedelta
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

def create_playlist(session_id):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    user = get_current_user_id(session_id)

    spotify.user_playlist_create(user,name="Your Recommended Playlist", public=False, collaborative=True, description="This is the playlist to reflect your selected playlist. Hope you enjoy listen it.")


def add_tracks_to_playlist(session_id, user_id, playlist_id, tracks):
    tokens = get_user_tokens(session_id)
    spotify = spotipy.Spotify(auth=tokens.access_token)

    spotify.user_playlist_add_tracks(user_id,playlist_id, tracks)








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

def extract_data(session_id,playlistDF, playlist_id):
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


def drop_duplicates(df):
    '''
    Drop duplicate songs
    '''
    df['artists_song'] = df.apply(lambda row: row['artist_name']+row['track_name'],axis = 1)
    return df.drop_duplicates('artists_song')

def getSubjectivity(text):
  '''
  Getting the Subjectivity using TextBlob
  '''
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  '''
  Getting the Polarity using TextBlob
  '''
  return TextBlob(text).sentiment.polarity

def getAnalysis(score, task="polarity"):
  '''
  Categorizing the Polarity & Subjectivity score
  '''
  if task == "subjectivity":
    if score < 1/3:
      return "low"
    elif score > 1/3:
      return "high"
    else:
      return "medium"
  else:
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'


def sentiment_analysis(df, text_col):
  '''
  Perform sentiment analysis on text
  ---
  Input:
  df (pandas dataframe): Dataframe of interest
  text_col (str): column of interest
  '''
  df['subjectivity'] = df[text_col].apply(getSubjectivity).apply(lambda x: getAnalysis(x,"subjectivity"))
  df['polarity'] = df[text_col].apply(getPolarity).apply(getAnalysis)
  return df  

def ohe_prep(df, column, new_name): 
    ''' 
    Create One Hot Encoded features of a specific column
    ---
    Input: 
    df (pandas dataframe): Spotify Dataframe
    column (str): Column to be processed
    new_name (str): new column name to be used
        
    Output: 
    tf_df: One-hot encoded features 
    '''
    
    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)    
    return tf_df

def create_feature_set(df, float_cols):
    '''
    Process spotify df to create a final set of features that will be used to generate recommendations
    ---
    Input: 
    df (pandas dataframe): Spotify Dataframe
    float_cols (list(str)): List of float columns that will be scaled
            
    Output: 
    final (pandas dataframe): Final set of features 
    '''
    
    # Tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix =  tfidf.fit_transform(df['genres'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    #genre_df.drop(columns='genre|unknown') # drop unknown genre
    genre_df.reset_index(drop = True, inplace=True)
    
    # Sentiment analysis
    df = sentiment_analysis(df, "track_name")

    # One-hot Encoding
    subject_ohe = ohe_prep(df, 'subjectivity','subject') * 0.3
    polar_ohe = ohe_prep(df, 'polarity','polar') * 0.5
    key_ohe = ohe_prep(df, 'key','key') * 0.5
    mode_ohe = ohe_prep(df, 'mode','mode') * 0.5

    # Normalization
    # Scale popularity columns
    pop = df[["artist_pop","track_pop"]].reset_index(drop = True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns = pop.columns) * 0.2 

    # Scale audio columns
    floats = df[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) * 0.2

    # Concanenate all features
    final = pd.concat([genre_df, floats_scaled, pop_scaled, subject_ohe, polar_ohe, key_ohe, mode_ohe], axis = 1)
    
    # Add song id
    final['track_id']=df['track_id'].values
    
    return final

def generate_playlist_feature(complete_feature_set, playlist_df):
    '''
    Summarize a user's playlist into a single vector
    ---
    Input: 
    complete_feature_set (pandas dataframe): Dataframe which includes all of the features for the spotify songs
    playlist_df (pandas dataframe): playlist dataframe
        
    Output: 
    complete_feature_set_playlist_final (pandas series): single vector feature that summarizes the playlist
    complete_feature_set_nonplaylist (pandas dataframe): 
    '''
    
    # Find song features in the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['track_id'].isin(playlist_df['track_id'].values)]
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['track_id'].isin(playlist_df['track_id'].values)]
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns = "track_id")
    return complete_feature_set_playlist_final.sum(axis = 0), complete_feature_set_nonplaylist


def generate_playlist_recos(df, features, nonplaylist_features):
    '''
    Generated recommendation based on songs in aspecific playlist.
    ---
    Input: 
    df (pandas dataframe): spotify dataframe
    features (pandas series): summarized playlist feature (single vector)
    nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist
        
    Output: 
    non_playlist_df_top_20: Top 20 recommendations for that playlist
    '''
    
    non_playlist_df = df[df['track_id'].isin(nonplaylist_features['track_id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('track_id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_20 = non_playlist_df.sort_values('sim',ascending = False).head(20)
    
    return non_playlist_df_top_20


def get_recommended_tracks(session_id,playlist_id):

    all_playlist_list = ["https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=253f12a3e38c4aa1","https://open.spotify.com/playlist/37i9dQZEVXbJARRcHjHcAr?si=3116bd59ece7457d",
                     "https://open.spotify.com/playlist/37i9dQZF1DX2iRL6tJD46O?si=e1634761eed1487c", "spotify:playlist:37i9dQZF1DX3iWJN79KKoY","spotify:playlist:37i9dQZF1DXc8YFRm3hen8", 
                     "spotify:playlist:37i9dQZF1DX28yPuNTio0f", "spotify:playlist:37i9dQZF1DWSDCcNkUu5tr","spotify:playlist:37i9dQZF1DWZjqjZMudx9T", "https://open.spotify.com/playlist/37i9dQZF1DWSnRSDTCsoPk?si=f8e34e93f2974aea"]

    all_playlistDF = pd.DataFrame()

    for playlist in range(len(all_playlist_list)):
        temp_playlist = pd.DataFrame()
        playlist_link = all_playlist_list[playlist]
        pl_id = playlist_link.split("/")[-1].split("?")[0]
        
        temp_playlist = extract_data(session_id,temp_playlist, pl_id)

        all_playlistDF = all_playlistDF.append(temp_playlist)


    user_playlistDF = pd.DataFrame() 
    user_playlistDF = extract_data(session_id,user_playlistDF, playlist_id)

    playlistDF = pd.DataFrame()
    songDF = drop_duplicates(all_playlistDF)
    playlistDF = drop_duplicates(user_playlistDF)

    sentiment = sentiment_analysis(songDF, "track_name")

    # One-hot encoding for the subjectivity 
    subject_ohe = ohe_prep(sentiment, 'subjectivity','subject')

    # Save the data and generate the features
    float_cols = songDF.dtypes[songDF.dtypes == 'float64'].index.values

    floats = songDF[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) * 0.2

    # Test playlist:  User's Playlist
    playlistDF_test = playlistDF.copy()

    # Save the data and generate the features
    float_cols = songDF.dtypes[songDF.dtypes == 'float64'].index.values

    # Generate features
    complete_feature_set = create_feature_set(songDF, float_cols=float_cols)

    # Generate the features
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(complete_feature_set, playlistDF_test)

    # Genreate top 10 recommendation
    recommended_songs = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)

    return recommended_songs


