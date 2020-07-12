from insurance.models import UserRole, PermissionUser, Permission, PermissionRole, Role


def is_granted(user, permission_code_name):
    is_user_granted = PermissionUser.objects.filter(permission__code_name=permission_code_name,
                                                    user=user,
                                                    grant=True).exist()
    return is_user_granted
