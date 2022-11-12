from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from .models import User, Post
from rest_framework.response import Response
from rest_framework import status

class PostView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None):
        if id:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            print(serializer.data)
        else:
            post = Post.objects.filter(user=request.user.id).order_by('-created_ts')
            serializer = PostSerializer(post, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        data['user'] = str(request.user.id)
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {}
        response_data.update(serializer.data)
        response_data.pop('likes')
        response_data.pop('comments')

        return Response(response_data)
    
    def delete(self, request,id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.user.id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message":"Delete Successful"},status=status.HTTP_200_OK)

class PostLikeView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=request.user.id)
        if user in post.likes.all():
            return Response({'message':'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.add(user)
        return Response({'message':'Liked'}, status=status.HTTP_202_ACCEPTED)


class PostUnlikeView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=request.user.id)
        if user not in post.likes.all():
            return Response({'message':'You did not like this post'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.remove(user)
        return Response({'message':'Unliked'}, status=status.HTTP_202_ACCEPTED)

class PostCommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request,id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['user'] = str(request.user.id)
        data['post'] = post.id
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {}
        response_data.update(serializer.data)
        response_data.pop('user')
        response_data.pop('post')
        response_data.pop('created_ts')
        response_data.pop('body')
        return Response(response_data)