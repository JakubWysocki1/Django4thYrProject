from django.urls import path
from .views import signupView, signinView, signoutView, profileView


urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('profile/', profileView, name='profile'),
] 



