from xml.etree.ElementInclude import include
from django.urls import path
from . import views
app_name='main'



urlpatterns = [
    path('', views.home, name='home'),
    path('songs/<str:song_id>/', views.song_detail, name='songdetail'),
    path('toggle_comment_reaction/', views.toggle_comment_reaction, name='toggle_comment_reaction'),
    path('trendingSongs/', views.trendingSongs, name='trendingSongs')
] 