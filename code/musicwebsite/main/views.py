import spotipy
from django.shortcuts import render, redirect, get_object_or_404
import requests
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy import Spotify
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from .models import Comment


# Create your views here.
def authentication():
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a2be13064936401992b518216aade28c",
    #                                     client_secret="ef320547195a4b80b5fe92c931486723",
    #                                     redirect_uri="http://localhost:1234",
    #                                     scope="user-library-read"))
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a2be13064936401992b518216aade28c",
                                                           client_secret="ef320547195a4b80b5fe92c931486723"))
    
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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.song_id = song_id
            comment.save()
            return redirect('main:songdetail', song_id=song_id)
    else:
        form = CommentForm()
 
    if request.method == 'POST' and 'deleteComment' in request.POST:
        comment_id = request.POST.get('deleteComment')
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return redirect('main:songdetail', song_id=song_id)

    comments = Comment.objects.filter(song_id=song_id).order_by('-created_at')
    comment_count = comments.count()
    return render(request, 'songdetail.html', {'songinfo': songinfo, 'form': form, 'comments': comments, 'comment_count': comment_count})

    