from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    def get_likes(self,post):
        return post.likes.count()

    def get_comments(self,post):
        return [comment.body for comment in Comment.objects.filter(post=post)]
    class Meta:
        model = Post
        fields = ('id','title','description','created_ts','likes','user','comments')
        extra_kwargs = {"user": {"write_only": True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','user','post','created_ts','body')



