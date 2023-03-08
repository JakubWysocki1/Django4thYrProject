from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', ]



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)