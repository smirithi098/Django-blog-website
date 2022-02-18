from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=150, null=False)
    subtitle = models.CharField(max_length=250, null=False)
    content = models.TextField(null=False)
    tag = models.CharField(max_length=20, null=False)
    image_url = models.URLField(max_length=300,
                                default="https://images.pexels.com/photos/267569/pexels-photo-267569.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200")
    date_posted = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-posts-list')
