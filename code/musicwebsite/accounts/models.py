from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    

    def __str__(self):
        return self.user.username