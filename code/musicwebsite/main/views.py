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
from country_converter import CountryConverter
from django.urls import reverse
import requests
from django.conf import settings
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
import json
import statistics

# Create your views here.
def authentication():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=settings.SPOTIPY_CLIENT_ID,
                                                           client_secret=settings.SPOTIPY_CLIENT_SECRET))
    
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

    referer_url = request.META.get('HTTP_REFERER')

    if "trendingSongs" in referer_url:
        referer_name = "Trending Songs"
    elif "newReleases" in referer_url:
        referer_name = "New Releases"
    elif "albumDetail" in referer_url:
        referer_name = "Album"
    elif "ratingstats" in referer_url:
        referer_name = "Rating Statistics"

    else:
        referer_name = "?"

    uri = 'spotify:track:' + song_id
    songinfo = sp.track(uri)

    comments = Comment.objects.filter(song_id=song_id).order_by('-created_at')
    comment_count = comments.count()

    ratings = Review.objects.filter(song_id=song_id)
    if ratings.exists():
        average_rating = round(ratings.aggregate(Avg('rating'))['rating__avg'], 1)
    else:
        average_rating = "-"
    rating_count = ratings.count()

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

        elif 'addRating' in request.POST:
            ratingVal = request.POST.get('addRating')
            if ratingVal:
                rating = Review.objects.create(
                user=request.user,
                song_id=song_id,
                rating=ratingVal,)
            messages.success(request, 'Rating Added!')
            return redirect('main:songdetail', song_id=song_id)
            
    return render(request, 'songdetail.html', {'songinfo': songinfo, 'form': form, 'comments': comments, 
                                               'comment_count': comment_count, 'editform': editform, 'replyform': replyform, 
                                               'editreplyform': editreplyform, 'average_rating': average_rating, 'rating_count':rating_count,'refererurl': referer_url, 'referername': referer_name})

def trendingSongs(request):
    sp = authentication()

    genras = sp.recommendation_genre_seeds()['genres']
    genras = sorted(genras)

    country_codes = sp.available_markets()['markets']
    
    countries = CountryConverter().convert(names=country_codes, to='name_short')


    finalcountries =[]

    for i in range(len(country_codes)):
        if countries[i] == "Türkiye":
            countries[i] = "Turkey"
        if countries[i] == "United States":
            countries[i] = "USA"

        finalcountries.append([country_codes[i],countries[i]])
    # for code in country_codes:
    #     country  = pycountry.countries.get(alpha_2=code)
    #     if country is not None:
    #         country = country.name 
    #         templist = []
    #         templist.append(country)
    #         templist.append(code)
    #         countries.append(templist)   

    top_songsGlobalURI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    
    top_songsResults = sp.playlist_tracks(top_songsGlobalURI)

    topsongs = top_songsResults['items']

    while top_songsResults['next']:
        top_songsResults = sp.next(top_songsResults)
        topsongs.extend(top_songsResults['items'])



    results = sp.search(q='top afropop', type='playlist', limit=1)
   

       
    # categories = sp.categories(country='US', limit=50)['categories']['items']
    # print({category['name']: category['id'] for category in categories})

    return render(request, 'trendingSongs.html', { 'genras': genras, 'countries': finalcountries, 'topsongs': topsongs})


def newReleases(request):

    sp = authentication()

    genras = ['test']
    country_codes = sp.available_markets()['markets']
    
    countries = CountryConverter().convert(names=country_codes, to='name_short')

    finalcountries =[]

    for i in range(len(country_codes)):
        if countries[i] == "Türkiye":
            countries[i] = "Turkey"
        if countries[i] == "United States":
            countries[i] = "USA"
               
        finalcountries.append([country_codes[i],countries[i]])

    new_releasesresults = sp.new_releases(limit=50)
    new_releases = new_releasesresults
    trackslist =[]
    for album in new_releases['albums']['items']:
        if album['album_group'] == "single":
            
            tracks = sp.album_tracks(album['id'])
            id = tracks['items'][0]['id']
            track = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'url': 'main:songdetail',
                'id': id,
                'image': album['images'][2]['url'] if album['images'] else None
            }
            trackslist.append(track)
        else:
           
            track = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'url': 'main:album_detail',
                'id': album['id'],
                'albumimage': album['images'][2]['url'] if album['images'] else None,
                'albumname': album['name'],
                'image': album['images'][2]['url'] if album['images'] else None
            }
            trackslist.append(track)

    
    
    return render(request, 'newReleases.html', {'genres': genras, 'countries':finalcountries, 'tracks': trackslist})

def albumDetail(request, album_id):
    sp = authentication()
    tracks = sp.album_tracks(album_id)
    album_image = request.GET.get('album_image')
    album_name = request.GET.get('album_name')
    trackslist =[]
    for track in tracks['items']:
        
        artist = track['artists'][0]['name']
        if len(track['artists']) > 1:
            artists= []
            for artist in track['artists']:
                artists.append(artist['name'])
            artist = ', '.join(artists)        
        track = {
            'name': track['name'],
            'artist': artist,
            'id': track['id'],
            'image': album_image
        }
        trackslist.append(track)
    return render(request, 'albumdetail.html', {'tracks': trackslist, 'album_name':album_name,})


def getNewReleases(request):
    sp = authentication()


    country = request.GET.get('country')
    genre = request.GET.get('genre')
    type = request.GET.get('type')
    print(country)
    
   
    if country == "global":
        country = None

    new_releases = sp.new_releases(country=country, limit=50)
    trackslist =[]
    for album in new_releases['albums']['items']:
        if album['album_group'] == "single":
            
            tracks = sp.album_tracks(album['id'])
            id = tracks['items'][0]['id']
            track = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'url': reverse('main:songdetail', args=[id]),
                'id': id,
                'image': album['images'][2]['url'] if album['images'] else None
            }
            trackslist.append(track)
        else:
            track = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'url': reverse('main:album_detail', args=[album['id']]),
                'id': album['id'],
                'albumimage': album['images'][2]['url'] if album['images'] else None,
                'albumname': album['name'],
                'image': album['images'][2]['url'] if album['images'] else None
            }
            trackslist.append(track)

    # Do something with the selected values
    response_data = {'tracks': trackslist}

    return JsonResponse(response_data)


def getTrendinSongs(request):
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
                print(playlist)
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
                        'image': track['track']['album']['images'][1]['url'] if track['track']['album']['images'] else None
                    }
                    tracks.append(track)

                return JsonResponse({'tracks': tracks})
            
            else:
                tracks = []
            
        return JsonResponse({'tracks': tracks})

 
def ratingStats(request, song_id):
    sp = authentication()

    songinfo = sp.track(song_id)


    ratings = Review.objects.filter(song_id=song_id)
    ratings_dict = {i: 0 for i in range(1, 11)}  # initialize counts to 0 for all possible ratings (1-10)

    # Count the ratings
    ratings_list = []
    for review in ratings:
        rating = review.rating
        ratings_list.append(rating)
        ratings_dict[rating] += 1

    print(len(ratings_list))

    if len(ratings_list) == 0:
        mean_rating = 0
        mode_rating = 0
        median_rating = 0
    else:
        mean_rating = round(statistics.mean(ratings_list), 1)
        mode_rating = round(statistics.mode(ratings_list), 1)
        median_rating = round(statistics.median(ratings_list), 1)


    

    # Convert the ratings count to a list of dictionaries
    ratings_list = [{'rating': rating, 'votes': count} for rating, count in ratings_dict.items()]

    # Sort the ratings list by descending order of votes
    ratings_list.sort(key=lambda x: x['rating'], reverse=True)
    ratings_json = json.dumps(ratings_list)

    return render(request, "ratingStats.html", {'ratings': ratings_json, 'songinfo': songinfo, 'meanrating': mean_rating, 'medianrating': median_rating, 'moderating':mode_rating})




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