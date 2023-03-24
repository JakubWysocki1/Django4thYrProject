from xml.etree.ElementInclude import include
from django.urls import path
from . import views
app_name='main'



urlpatterns = [
    
    path('', views.api, name='home'),
    path('songs/<str:song_id>', views.song_detail, name='songdetail'),
]