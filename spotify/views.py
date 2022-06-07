from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import os
from rest_framework.views import APIView
from requests import Request, Response, post, session
from rest_framework import status
from rest_framework.response import Response
from  .util import *
from django.views import *
from django.urls import reverse
# Create your views here.

class AuthURL(APIView):
    
    def get(self, request, format=None):
        scopes = 'playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'client_id': os.getenv('SPOTIFY_CLIENT_ID')
        }).prepare().url

        return Response({'url': url}, status= status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET')
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, refresh_token, expires_in)

    return redirect('frontend:my-playlists')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)

        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class GetUserPlaylists(APIView):
    def get(self, request, format=None):
        session_id = self.request.session.session_key
        endpoint = "me/playlists"
        response = execute_spotify_api_request(session_id, endpoint)
        return Response(response , status=status.HTTP_200_OK)

class GetPlaylist(APIView):
    def get(self, request, format=None):
        session_id = self.request.session.session_key
        response = get_playlist(session_id)

        #print(response)
        #total = response["total"]
        
        playlist = []
        pl_songs = []

        for i in range(len(response['items'])):

            playlist_id = response['items'][i]['id']
            songs_list = get_playlist_songs(session_id,playlist_id)
            #total_songs = songs_list['total']
            for j in range(len(songs_list['items'])):
                pl_songs.append(
                    {
                        'name': songs_list['items'][j]['track']['name'],
                        'artist': songs_list['items'][j]['track']['album']['artists'][0]['name'],
                        'img': songs_list['items'][j]['track']['album']['images'][0]['url']
                    }
                )
            
            playlist.append(
            {   'name': response['items'][i]['name'],
                'cover': response['items'][i]['images'][0]['url'],
                'id': response['items'][i]['id'],
                'owner': response['items'][i]['owner']['display_name'],
                'songs': pl_songs,
            }
            )

            pl_songs = []

        '''playlists = [{
            'items': items,
            'total': total,
            'names': names,
            'cover': cover,
            'id': playlist_id}]'''

        #print(playlist[0]['songs'])
        return Response(playlist, status=status.HTTP_200_OK)

#instead of getting playlists' songs in another view, 
#now we are getting these datas in the same view with get_playlists view.

class GetPlaylistSongs(APIView):
    def get(self, request,format=None):
        session_id = self.request.session.session_key
        playlist_id = "4U20aqvtwc1jYA847xQCMA"

        if playlist_id is None:
            playlist_id = "dsfaf"

        response = get_playlist_songs(session_id,playlist_id)

        return Response(response, status=status.HTTP_200_OK)


class MakePlaylistRecommendation(APIView):
    def get(self, request, id):
        session_id = self.request.session.session_key
    
        pl_songs = []

        def extract_data(playlistDF, playlist_URI):
            sp = spotipy.Spotify(auth=get_user_tokens(session_id).access_token)
            for track in sp.playlist_tracks(playlist_URI)["items"]:
                try:
                    track_id = track["track"]["id"]
                    track_name = track["track"]["name"]

                    track_pop = track["track"]["popularity"]

                    #Main Artist
                    artist_uri = track["track"]["artists"][0]["uri"]
                    artist_info = sp.artist(artist_uri)
                    artist_name = track["track"]["artists"][0]["name"]
                    artist_pop = artist_info["popularity"]
                    genres = artist_info['genres']

                    for feature in sp.audio_features(track["track"]["id"]):
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

                    ser = pd.Series([track_id, track_name, track_pop ,artist_name, artist_pop, genres, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo])
                    playlistDF = pd.concat([playlistDF, ser],axis = 1, ignore_index = True)


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

        all_playlist_list = ["https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=253f12a3e38c4aa1","https://open.spotify.com/playlist/37i9dQZEVXbJARRcHjHcAr?si=3116bd59ece7457d",
                            "https://open.spotify.com/playlist/37i9dQZF1DX2iRL6tJD46O?si=e1634761eed1487c", "spotify:playlist:37i9dQZF1DX3iWJN79KKoY","spotify:playlist:37i9dQZF1DXc8YFRm3hen8", 
                            "spotify:playlist:37i9dQZF1DX28yPuNTio0f", "spotify:playlist:37i9dQZF1DWSDCcNkUu5tr","spotify:playlist:37i9dQZF1DWZjqjZMudx9T"]

        # Extracting all data
        all_playlistDF = pd.DataFrame()

        #for playlist in range(len(all_playlist_list)):
        for playlist in range(2):
            temp_playlist = pd.DataFrame()
            playlist_link = all_playlist_list[playlist]
            playlist_URI = playlist_link.split("/")[-1].split("?")[0]
            #track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
            
            temp_playlist = extract_data(temp_playlist, playlist_URI)

            all_playlistDF = all_playlistDF.append(temp_playlist)

            
        user_playlistDF = pd.DataFrame() 

        user_playlistDF = extract_data(user_playlistDF, id)

        playlistDF = pd.DataFrame()
        # Drop song duplicates
        def drop_duplicates(df):
            '''
            Drop duplicate songs
            '''
            df['artists_song'] = df.apply(lambda row: row['artist_name']+row['track_name'],axis = 1)
            return df.drop_duplicates('artists_song')
        print(all_playlistDF['genres'].dtype)
        songDF = drop_duplicates(all_playlistDF)
        playlistDF = drop_duplicates(user_playlistDF)

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
        # Show result
        sentiment = sentiment_analysis(songDF, "track_name")

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
            non_playlist_df_top_20 = non_playlist_df.sort_values('sim',ascending = False, ignore_index = True).head(20)
            
            return non_playlist_df_top_20

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
        recommend = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)  
        '''
        for i in range(recommend.shape[0]):
            pl_songs.append({
                'name': recommend.loc[i,'track_name'],
                'id': recommend.loc[i, 'track_id'],
                'artist': recommend.loc[i,'artist_name']
            })
        '''
        for i in range(recommend.shape[0]):
            pl_songs.append(recommend.loc[i, 'track_id'])

        
        #Now its time to create a recommended playlist on the user's account

        create_playlist(session_id)
        user_playlists = get_playlist(session_id)
        new_playlist_id = user_playlists['items'][0]['id']

        add_tracks_to_playlist(session_id, get_current_user_id(session_id), new_playlist_id, pl_songs)
        
        new_pl_songs = []
        
        songs_list = get_playlist_songs(session_id,new_playlist_id)
        total_songs = songs_list['total']
        for j in range(total_songs):
            new_pl_songs.append(
                {
                    'name': songs_list['items'][j]['track']['name'],
                    'artist': songs_list['items'][j]['track']['album']['artists'][0]['name'],
                    'img': songs_list['items'][j]['track']['album']['images'][0]['url']
                }
            )
 
        return Response(new_pl_songs, status=status.HTTP_200_OK)

def DeletePlaylistView(request):
    session_id = request.session.session_key

    delete_recommended_playlist(session_id)   

    return redirect('frontend:my-playlists') 