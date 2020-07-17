from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from insurance import util
from insurance.models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['roles'] = util.get_user_roles(self.user)
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'