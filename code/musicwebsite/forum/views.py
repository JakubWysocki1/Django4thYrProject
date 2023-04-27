from django.shortcuts import render
from .models import ForumCategory, ForumPost
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone
from .forms import ForumPostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.


def forumtopics(request):
    forumcategory = ForumCategory.objects.all()


    return render(request, 'forumtopics.html', {'forumcategories':forumcategory})


def categoryposts(request, category_name):

    try:
        forumcategory = ForumCategory.objects.get(name=category_name)
        forumpost = ForumPost.objects.filter(category=forumcategory).all().order_by('-created_at')

        now = timezone.now()
        for post in forumpost:
            post.time_since_created = timesince(post.created_at, now)

        
        forumpostform = ForumPostForm()
        editform = ForumPostForm()

        if request.method == 'POST':
            if "postTopic" in request.POST:
                forumpostform = ForumPostForm(request.POST)
                if forumpostform.is_valid():
                    post = forumpostform.save(commit=False)
                    post.user = request.user
                    post.category = forumcategory
                    post.save()
                    messages.success(request, 'Topic Added!')
                    return redirect('forum:categoryposts', category_name)
            elif "deleteTopic" in request.POST:
                post_id = request.POST.get('deleteTopic')
                post = get_object_or_404(ForumPost, id=post_id, user=request.user)
                post.delete()
                messages.success(request, 'Comment Deleted!')
                return redirect('forum:categoryposts', category_name)
            elif "editTopic" in request.POST:
                post_id = request.POST.get('editTopic')
                post = get_object_or_404(ForumPost, id=post_id, user=request.user)
                editform = ForumPostForm(request.POST, instance=post)
                if editform.is_valid():
                    editform.save()
                    messages.success(request, 'Topic Updated!')
                    return redirect('forum:categoryposts', category_name)


        return render(request, 'categoryposts.html', {'category_name': category_name, 'posts':forumpost, 'forumPostForm': forumpostform, 'editpost':editform})
    
    except ForumCategory.DoesNotExist as e:
        invalid_id = "Category does not exist"
        
        return render(request, 'categoryposts.html', {'invalid_id': invalid_id ,'category_name': "", 'posts': "", 'forumPostForm': "", 'editpost':""})




def post(request, category_name, post_id):
    try:
        forumcategory = ForumCategory.objects.get(name=category_name)
        forumpost = ForumPost.objects.get(id=post_id, category=forumcategory)
    
        return render(request, 'post.html', {'post': forumpost, 'category_name': category_name,})

    
    except ForumPost.DoesNotExist or ForumCategory.DoesNotExist:
        
        invalid_id = "Post ID or category does not exist"
        return render(request, 'post.html', {'invalid_id':invalid_id,'post': ""})
    
