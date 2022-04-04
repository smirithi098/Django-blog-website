from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile-pic-3.png', upload_to="profile-images")
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CustomSession(models.Model):
    session_key = models.CharField(max_length=40)
    otp_field = models.CharField(max_length=6)
    created_time = models.TimeField(auto_now_add=True)