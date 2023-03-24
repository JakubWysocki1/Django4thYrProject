import spotipy
from django.shortcuts import render
import requests
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

# Create your views here.
def authentication():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a2be13064936401992b518216aade28c",
                                        client_secret="ef320547195a4b80b5fe92c931486723",
                                        redirect_uri="http://localhost:1234",
                                        scope="user-library-read"))
    
    return sp


def home(request):
    return render(request, 'music/home.html')

def api(request):
    sp = authentication()



    top_songsGlobalURI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    top_songsResults = sp.playlist_tracks(top_songsGlobalURI)
    # print(top_songsResults)
    topsongs = top_songsResults['items']
    

    # taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
    # results = sp.artist_albums(taylor_uri, album_type='album')
    # albums = results['items']
        
    while top_songsResults['next']:
        top_songsResults = sp.next(top_songsResults)
        topsongs.extend(top_songsResults['items'])
    
    #print(albums[0])
    return render(request, 'home.html', {'topsongs':topsongs})

def song_detail(request, song_id):
    sp = authentication()

    uri = 'spotify:track:' + song_id
    songinfo = sp.track(uri)
    print(songinfo)

    
    
    return render(request, 'songdetail.html', {'songinfo': songinfo})
