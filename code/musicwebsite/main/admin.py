from django.contrib import admin
from .models import Comment, CommentReply, Review
# Register your models here.
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Review)