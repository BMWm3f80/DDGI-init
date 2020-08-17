from django.contrib import admin
from insurance.models import *
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_name', 'title')
    readonly_fields = ('cr_by', 'cr_on', 'up_by', 'up_on')

    def save_model(self, request, obj, form, change):
        if change:
            obj.up_by = request.user
        else:
            obj.cr_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    readonly_fields = ('cr_by', 'cr_on')

    def save_model(self, request, obj, form, change):
        if change:
            obj.cr_by = request.user
        else:
            obj.cr_by = request.user
        permissions = PermissionRole.objects.filter(role=obj.role)
        for p in permissions:
            PermissionUser.objects.create(permission=p.permission,
                                          user=obj.user,
                                          grant=p.grant,
                                          cr_by=request.user)
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            permission_ids = PermissionRole.objects.filter(role=obj.role).values_list('permission_id')
            PermissionUser.objects.filter(user=obj.user, permission__in=permission_ids).delete()
            obj.delete()


@admin.register(PermissionRole)
class PermissionRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'role')

    def save_model(self, request, obj, form, change):
        if change:
            obj.cr_by = request.user
        else:
            obj.cr_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PermissionUser)
class PermissionUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission', 'grant')

    def save_model(self, request, obj, form, change):
        if change:
            obj.cr_by = request.user
        else:
            obj.cr_by = request.user
        super().save_model(request, obj, form, change)



