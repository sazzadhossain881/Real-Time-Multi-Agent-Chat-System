from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import UserSerializer, UserSerializerWithToken
from rest_framework import status

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
       data = super().validate(attrs)
       data.pop('refresh', None)
       data.pop('access', None)

       serializer = UserSerializerWithToken(self.user).data
       for key, value in serializer.items():
           data[key] = value

       return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializerWithToken(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
