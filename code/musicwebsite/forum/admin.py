from django.contrib import admin
from .models import ForumCategory, ForumPost

# Register your models here.
admin.site.register(ForumCategory)
admin.site.register(ForumPost)
