from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='forum'

urlpatterns = [
    path('', views.forumtopics, name='forumtopics'),
    path('<str:category_name>/', views.categoryposts, name='categoryposts'),
    path('<str:category_name>/post/<str:post_id>/', views.post, name='post'),

   
] 