from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    "serializer for the user"
    is_admin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff
    
class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password', 'token']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

