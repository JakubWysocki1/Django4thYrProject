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
    sp = authentication()

    top_songsGlobalURI = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    top_songsResults = sp.playlist_tracks(top_songsGlobalURI)

    topsongs = top_songsResults['items']
    
    while top_songsResults['next']:
        top_songsResults = sp.next(top_songsResults)
        topsongs.extend(top_songsResults['items'])


    
    #print(albums[0])
    return render(request, 'home.html', {'topsongs':topsongs,})

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

    top_songsSpainURI = 'spotify:playlist:37i9dQZEVXbNFJfN1Vw8d9'
    top_songsFranceURI = 'spotify:playlist:37i9dQZEVXbIPWwFssbupI'

    top_spainsongsResults = sp.playlist_tracks(top_songsSpainURI)
    top_francesongsResults = sp.playlist_tracks(top_songsFranceURI)

    topfrancesongs = top_francesongsResults['items']
    topspainsongs = top_spainsongsResults['items']

    while top_spainsongsResults['next']:
        top_spainsongsResults = sp.next(top_spainsongsResults)
        topspainsongs.extend(top_spainsongsResults['items'])

    while top_francesongsResults['next']:
        top_francesongsResults = sp.next(top_francesongsResults)
        topfrancesongs.extend(top_francesongsResults['items'])

    return render(request, 'trendingSongs.html', { 'topspainsongs': topspainsongs,'topfrancesongs': topfrancesongs})


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