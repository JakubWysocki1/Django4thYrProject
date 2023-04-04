from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.



class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg',upload_to='profile_pictures')
    bio = models.TextField(max_length=1500, blank=True)
    

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)