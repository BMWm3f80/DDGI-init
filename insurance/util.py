from insurance.models import UserRole, PermissionUser, Permission, PermissionRole, Role, Profile
from insurance import serializers


def is_granted(user, permission_code_name):
    is_user_granted = PermissionUser.objects.filter(permission__code_name=permission_code_name,
                                                    user=user,
                                                    grant=True).exist()
    return is_user_granted


def get_user_roles(user):
    userroles = UserRole.objects.filter(user=user)
    serializer = serializers.UserRoleSerializer(userroles, many=True, read_only=True)
    return serializer.data


def get_user_profile(user):
    profile = Profile.objects.get(user=user)
    serializer = serializers.ProfileSerializer(profile)
    return serializer.data


def get_user_permissions(user):
    userpermissions = PermissionUser.objects.filter(user=user, grant=True)
    serializer = serializers.PermissionUserSerializer(userpermissions, many=True, read_only=True)
    return serializer.data
