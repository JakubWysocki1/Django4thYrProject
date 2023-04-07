from django.urls import path
from .views import signupView, signinView, signoutView, profileView, spotify_stats, profileDetailsView, spotify_callback, spotify_authorize
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('profile/<str:profile_name>', profileView, name='profile'),
    path('details/<str:profile_name>', profileDetailsView, name='profileDetails'),
    path('spotifyStats/', spotify_stats, name='spotifyStats'),
    path('spotifyStats/callback/', spotify_callback, name='spotifyCallback'),
    path('spotifyStats/authorize/', spotify_authorize, name='spotify_authorize'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

