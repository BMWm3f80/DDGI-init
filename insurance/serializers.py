from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from insurance import util
from django.contrib.auth.models import User
from insurance.models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['userdata'] = util.get_user_profile(self.user)
        data['roles'] = util.get_user_roles(self.user)
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'position', 'middle_name')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'code_name', 'title')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'title', 'is_active')



