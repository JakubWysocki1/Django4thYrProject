from django.urls import path
from .views import signupView, signinView, signoutView, profileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('profile/', profileView, name='profile'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

