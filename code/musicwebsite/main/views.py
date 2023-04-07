import spotipy
from django.shortcuts import render, redirect, get_object_or_404
import requests
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy import Spotify
from django.shortcuts import get_object_or_404
from .forms import CommentForm, ReplyForm, EditReplyForm
from .models import Comment, Review, CommentReply
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
import pycountry


# Create your views here.
def authentication():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a2be13064936401992b518216aade28c",
                                                           client_secret="ef320547195a4b80b5fe92c931486723"))
    
    return sp


def home(request):
    
    #print(albums[0])
    return render(request, 'home.html')

def search_tracks(request):
    # Get the user's search query from the request
    query = request.GET.get('query')

    # Make a search request to the Spotify Web API using the Spotipy client
    sp = authentication()
    results = sp.search(q=query, type='track')

    # Extract the track names from the search results
    tracks = []
    for item in results['tracks']['items']:
        print(item['id'])
        track = {
            'name': item['name'],
            'artist': item['artists'][0]['name'],
            'id': item['id'],
            'image': item['album']['images'][2]['url'] if item['album']['images'] else None
        }
        tracks.append(track)

    # Return the track names as a JSON response
    return JsonResponse({'tracks': tracks})

def song_detail(request, song_id):
    sp = authentication()

    uri = 'spotify:track:' + song_id
    songinfo = sp.track(uri)

    comments = Comment.objects.filter(song_id=song_id).order_by('-created_at')
    comment_count = comments.count()

    ratings = Review.objects.filter(song_id=song_id)
    form = CommentForm()
    editform = CommentForm()
    replyform = ReplyForm()
    editreplyform = EditReplyForm()

    if request.method == 'POST':
        if 'addComment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.song_id = song_id
                comment.save()
                messages.success(request, 'Comment Added!')
                return redirect('main:songdetail', song_id=song_id)
        elif 'deleteComment' in request.POST:
            comment_id = request.POST.get('deleteComment')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            messages.warning(request, 'Comment Deleted!')
            return redirect('main:songdetail', song_id=song_id)
        
        elif 'editComment' in request.POST:
            comment_id = request.POST.get('editComment')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            editform = CommentForm(request.POST, instance=comment)
            if editform.is_valid():
                editform.save()
                messages.success(request, 'Comment Updated!')
                return redirect('main:songdetail', song_id=song_id)
            
        elif 'parent_comment_id' in request.POST:
            print('parent_comment_id')
            replyform = ReplyForm(request.POST)
            if replyform.is_valid():
                reply = replyform.save(commit=False)
                reply.user = request.user
                reply.comment_id = replyform.cleaned_data['parent_comment_id']
                reply.save()
                messages.success(request, 'Reply Posted!')
                return redirect('main:songdetail', song_id=song_id)
            
        elif 'deleteReply' in request.POST:
            reply_id = request.POST.get('deleteReply')
            print('deletereply')
            reply = get_object_or_404(CommentReply, id=reply_id, user=request.user)
            reply.delete()
            messages.warning(request, 'Reply Deleted!')
            return redirect('main:songdetail', song_id=song_id)

        elif 'editReply' in request.POST:
            reply_id = request.POST.get('editReply')
            reply = get_object_or_404(CommentReply, id=reply_id, user=request.user)
            editreplyform = EditReplyForm(request.POST, instance=reply)
            if editreplyform.is_valid():
                editreplyform.save()
                messages.success(request, 'Reply Updated!')
                return redirect('main:songdetail', song_id=song_id)
            
    return render(request, 'songdetail.html', {'songinfo': songinfo, 'form': form, 'comments': comments, 'comment_count': comment_count, 'editform': editform, 'replyform': replyform, 'editreplyform': editreplyform})

def trendingSongs(request):
    sp = authentication()

    genras = sp.recommendation_genre_seeds()['genres']
    genras = sorted(genras)

    country_codes = sp.available_markets()['markets']
    
    countries = []
 
    for code in country_codes:
        country  = pycountry.countries.get(alpha_2=code)
        if country is not None:
            templist = []
            templist.append(country.name)
            templist.append(code)
            countries.append(templist)
        
    
    countries = sorted(countries, key=lambda x: x[0])

    top_songsGlobalURI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    
    top_songsResults = sp.playlist_tracks(top_songsGlobalURI)

    topsongs = top_songsResults['items']

    while top_songsResults['next']:
        top_songsResults = sp.next(top_songsResults)
        topsongs.extend(top_songsResults['items'])

    return render(request, 'trendingSongs.html', { 'genras': genras, 'countries': countries, 'topsongs': topsongs})


def searchPlaylist(request):
    sp = authentication()

    category_id = 'toplists'
    country_code = request.GET.get('countryCode')
    country_name = request.GET.get('countryName')
    print(country_name, country_code)
    

    # Get the playlists for the "Top Lists" category in the given country
    

    if country_name == "The World":
        top_songsGlobalURI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    
        playlistresults = sp.playlist_tracks(top_songsGlobalURI)

        playlistitem = playlistresults['items']
        tracks = []
        playlist_url = {'playlist_url': 'https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=aa665591baa647ca'}
        tracks.append(playlist_url)

        while playlistresults['next']:
            playlistresults = sp.next(playlistresults)
            playlistitem.extend(playlistresults['items'])

        for track in playlistitem:
                    
            track = {
                'name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'id': track['track']['id'],
                'image': track['track']['album']['images'][2]['url'] if track['track']['album']['images'] else None
            }
            tracks.append(track)

        return JsonResponse({'tracks': tracks})
        
    else: 
        playlists = sp.category_playlists(category_id, country=country_code)
    # Filter the playlists by name and owner
        for playlist in playlists['playlists']['items']:
            
            
            if "Your daily update of the most played tracks right now - "+ country_name in playlist['description']:
                playlistresults = sp.playlist_tracks(playlist['id'])
                playlistitem = playlistresults['items']
                
                
                while playlistresults['next']:
                    playlistresults = sp.next(playlistresults)
                    playlistitem.extend(playlistresults['items'])
                
                tracks = []
                playlist_url = {'playlist_url': playlist['external_urls']['spotify']}
                tracks.append(playlist_url)
                
                for track in playlistitem:
                    
                    track = {
                        'name': track['track']['name'],
                        'artist': track['track']['artists'][0]['name'],
                        'id': track['track']['id'],
                        'image': track['track']['album']['images'][2]['url'] if track['track']['album']['images'] else None
                    }
                    tracks.append(track)

                return JsonResponse({'tracks': tracks})
            
            else:
                tracks = []
            
        return JsonResponse({'tracks': tracks})

 


def toggle_comment_reaction(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        reaction_type = request.POST.get('reaction_type')
        comment = get_object_or_404(Comment, id=comment_id)

        if reaction_type == 'like':
            if request.user in comment.liked_by.all():
                comment.liked_by.remove(request.user)
                comment.likes -= 1
            else:
                comment.liked_by.add(request.user)
                comment.likes += 1
                if request.user in comment.disliked_by.all():
                    comment.disliked_by.remove(request.user)
                    comment.dislikes -= 1
        elif reaction_type == 'dislike':
            if request.user in comment.disliked_by.all():
                comment.disliked_by.remove(request.user)
                comment.dislikes -= 1
            else:
                comment.disliked_by.add(request.user)
                comment.dislikes += 1
                if request.user in comment.liked_by.all():
                    comment.liked_by.remove(request.user)
                    comment.likes -= 1

        comment.save()
        data = {'likes': comment.likes, 'dislikes': comment.dislikes}
        return JsonResponse(data)