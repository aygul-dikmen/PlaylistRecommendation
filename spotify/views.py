from django.shortcuts import render, redirect
import os
from rest_framework.views import APIView
from requests import Request, Response, post
from rest_framework import status
from rest_framework.response import Response
from  .util import *
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

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)

        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class GetUserPlaylists(APIView):
    def get(self, request, format=None):
        session_id = self.request.session.session_key
        endpoint = "me/playlists"
        response = execute_spotify_api_request(session_id, endpoint)
        #print(response)

        return Response(response , status=status.HTTP_200_OK)

class GetPlaylist(APIView):
    def get(self, request, format=None):
        session_id = self.request.session.session_key
        response = get_playlist(session_id)

        items = response["items"]
        total = response["total"]
        
        playlist = []

        for i in range(total):
            playlist.append(
            {'name': response['items'][i]['name'],
            'cover': response['items'][i]['images'][0]['url'],
            'id': response['items'][i]['id']}
            )
           

        '''playlists = [{
            'items': items,
            'total': total,
            'names': names,
            'cover': cover,
            'id': playlist_id}]'''

        return Response(playlist, status=status.HTTP_200_OK)