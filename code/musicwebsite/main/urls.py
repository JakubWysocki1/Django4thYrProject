from xml.etree.ElementInclude import include
from django.urls import path
from . import views
app_name='main'



urlpatterns = [
    path('', views.home, name='home'),
    path('songs/<str:song_id>/', views.song_detail, name='songdetail'),
    path('toggle_comment_reaction/', views.toggle_comment_reaction, name='toggle_comment_reaction'),
    path('trendingSongs/', views.trendingSongs, name='trendingSongs'),
    path('search/', views.search_tracks, name='search_tracks'),
    path('searchPlaylist/', views.getTrendinSongs, name='search_playlist'),
    path('searchGenra/', views.trendingGenras, name='search_genra'),
    path('newReleases/', views.newReleases, name='new_releases'),
    path('getNewReleases/', views.getNewReleases, name='get_new_releases'),     
    path('albumDetail/<str:album_id>', views.albumDetail, name='album_detail'),
] 