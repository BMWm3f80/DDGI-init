from insurance.models import UserRole, PermissionUser, Permission, PermissionRole, Role
from insurance import serializers


def is_granted(user, permission_code_name):
    is_user_granted = PermissionUser.objects.filter(permission__code_name=permission_code_name,
                                                    user=user,
                                                    grant=True).exist()
    return is_user_granted


def get_user_roles(user):
    serializer = serializers.UserRoleSerializer()
    return serializer.data