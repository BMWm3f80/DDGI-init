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
        data['permissions'] = util.get_user_permissions(self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserRoleSerializer(serializers.ModelSerializer):
    role_title = serializers.CharField(source="role.title")

    class Meta:
        model = UserRole
        fields = ('role_title',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    position_name = serializers.CharField(source="position")
    is_active = serializers.BooleanField(source="user.is_active")
    is_superuser = serializers.BooleanField(source="user.is_superuser")
    last_login = serializers.DateTimeField(source="user.last_login", format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Profile
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'position_name',
                  'middle_name',
                  'is_active',
                  'is_superuser',
                  'last_login')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionUserSerializer(serializers.ModelSerializer):
    permission_code = serializers.CharField(source="permission.code_name")
    class Meta:
        model = PermissionUser
        fields = ('permission_code', 'grant')



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'title', 'is_active')


class GridColSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridCols
        fields = ['title',
                  'data',
                  'name',
                  'type',
                  'width',
                  'searchable',
                  'orderable',
                  'className',
                  'defaultContent',
                  'visible']


class DtOptionSerializer(serializers.ModelSerializer):
    columns = GridColSerializer(many=True, read_only=True)

    class Meta:
        model = Dt_Option
        fields = ['codeName', 'title', 'dataPath', 'draw',
                  'keys', 'colReorder', 'fixedHeader', 'responsive',
                  'autoFill', 'serverSide', 'processing', 'scrollY', 'columns']


class IndividualClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualClient
        fields = '__all__'


class RegisteredPoliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredPolises
        fields = ['id', 'act_number', 'act_date', 'polis_number_from',
                  'polis_number_to', 'polis_quantity', 'polis_status',
                  'document']







