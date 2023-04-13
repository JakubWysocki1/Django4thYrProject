from django.shortcuts import render
from .models import ForumCategory, ForumPost
# Create your views here.


def forumtopics(request):
    forumcategory = ForumCategory.objects.all()


    return render(request, 'forumtopics.html', {'forumcategories':forumcategory})


def categoryposts(request, category_name):
    forumcategory = ForumCategory.objects.get(name=category_name)
    forumpost = ForumPost.objects.filter(category=forumcategory).all()

    return render(request, 'categoryposts.html', {'category_name': category_name, 'posts':forumpost})

def post(request, post_id):
    forumpost = ForumPost.objects.get(id=post_id)

    return render(request, 'post.html', {'post': forumpost})