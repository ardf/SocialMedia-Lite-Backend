from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from uuid import UUID

def is_valid_uuid(uuid_to_test, version=4):   
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

class FollowView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request,id=None):
        user = User.objects.get(id=request.user.id)
        if not is_valid_uuid(id):
            return Response({'message':'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        other_user = User.objects.filter(id=id).first()
        if other_user is None:
            return Response({'message':'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
        if other_user in user.following.all():
            return Response({'message':'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        user.following.add(other_user)
        return Response({'message':'Followed'}, status=status.HTTP_202_ACCEPTED)

class UnfollowView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request,id=None):
        user = User.objects.get(id=request.user.id)
        if not is_valid_uuid(id):
            return Response({'message':'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        other_user = User.objects.filter(id=id).first()
        print(other_user)
        if other_user is None:
            return Response({'message':'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
        if other_user not in user.following.all():
            return Response({'message':'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        user.following.remove(other_user)
        return Response({'message':'Unfollowed'}, status=status.HTTP_202_ACCEPTED)

