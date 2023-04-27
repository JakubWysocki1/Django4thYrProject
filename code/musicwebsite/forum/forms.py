from .models import ForumPost
from django import forms

class ForumPostForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your title...'})
        }


