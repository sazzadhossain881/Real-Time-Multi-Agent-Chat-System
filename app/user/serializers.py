from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    "serializer for the user"
    is_admin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'token']
        extra_kwargs = {
            'token':{
                'read_only':True,
            }
        }

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

