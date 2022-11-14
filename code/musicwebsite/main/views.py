import spotipy
from django.shortcuts import render
import requests
from spotipy.oauth2 import SpotifyOAuth

# Create your views here.


def home(request):
    return render(request, 'music/home.html')

def api(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a2be13064936401992b518216aade28c",
                                               client_secret="ef320547195a4b80b5fe92c931486723",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))

    taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
    results = sp.artist_albums(taylor_uri, album_type='album')
    albums = results['items']
        
    while results['next']:
         results = sp.next(results)
         albums.extend(results['items'])
         
    return render(request, 'music/home.html', {'albums':albums})
