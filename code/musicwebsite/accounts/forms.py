from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email',]

  
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class BioUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['bio']

    def clean_bio_text(self):
        bio_text = self.cleaned_data.get('bio')
        # Add any additional cleaning or validation code here
        return bio_text