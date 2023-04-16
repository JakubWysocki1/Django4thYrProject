from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

    def __str__(self):
        return self.text[0: 20]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.rating} - {self.user}'


class CommentReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:20]