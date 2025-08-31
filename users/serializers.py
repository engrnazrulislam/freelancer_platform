from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','first_name','last_name','email','password','address','phone_number','role']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','first_name', 'last_name','email','address','phone_number','role']
    
    def validate_role(self, value):
        if value == User.ADMIN:
            raise serializers.ValidationError("Admin role cannot be assigned via API.")
        return value