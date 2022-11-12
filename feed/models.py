from django.db import models
from account.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    created_ts = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_liked")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=128)
    created_ts = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.body
