from django import forms
from .models import Comment, CommentReply, Review
from django.core.validators import MinValueValidator, MaxValueValidator

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'})
        }

class ReplyForm(forms.ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CommentReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a reply...'})
        }

class EditReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a reply...'})
        }
