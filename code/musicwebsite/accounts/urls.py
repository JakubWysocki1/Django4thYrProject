from django.urls import path
from .views import signupView, signinView, signoutView, profileView, profileDetailsView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('profile/<str:profile_name>', profileView, name='profile'),
    path('details/<str:profile_name>', profileDetailsView, name='profileDetails'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

