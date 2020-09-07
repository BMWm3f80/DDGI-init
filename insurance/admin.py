from django.contrib import admin
from insurance.models import *
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserRoleInline(admin.TabularInline):
    model = UserRole
    verbose_name_plural = 'Roles'
    fk_name = 'user'
    extra = 0



class PermissionUserInline(admin.TabularInline):
    model = PermissionUser
    verbose_name_plural = 'Permissions'
    fk_name = 'user'
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, UserRoleInline, PermissionUserInline)

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


class PermissionRoleInline(admin.TabularInline):
    model = PermissionRole
    fk_name = 'role'
    verbose_name_plural = 'ROLE PERMISSIONS'
    verbose_name = 'PERMISSION'
    extra = 0


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    inlines = (PermissionRoleInline, )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    #readonly_fields = ('cr_by', 'cr_on')

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

    def delete_model(self, request, obj):
        permission_ids = PermissionRole.objects.filter(role=obj.role).values_list('permission_id')
        PermissionUser.objects.filter(user=obj.user, permission__in=permission_ids).delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            permission_ids = PermissionRole.objects.filter(role=obj.role).values_list('permission_id')
            PermissionUser.objects.filter(user=obj.user, permission__in=permission_ids).delete()
            obj.delete()



@admin.register(PermissionRole)
class PermissionRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')


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


class GridColsInline(admin.TabularInline):
    model = GridCols
    extra = 0
    fields = ('order_num', 'title', 'data', 'name', 'type', 'className', 'defaultContent',
              'width', 'searchable', 'orderable', 'visible')


@admin.register(Dt_Option)
class GridAdmin(admin.ModelAdmin):
    list_display = ('codeName', 'title')
    inlines = [GridColsInline]


@admin.register(IndividualClient)
class IndividualClientAdmin(admin.ModelAdmin):
    pass


@admin.register(RegisteredPolises)
class RegisteredPolises(admin.ModelAdmin):
    pass
