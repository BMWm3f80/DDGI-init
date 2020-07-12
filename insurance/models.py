from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Position(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=50)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должность'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, verbose_name='Должность', on_delete=models.CASCADE, null=True, blank=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50, null=True, blank=True)
    phone = models.CharField(verbose_name='Тел', max_length=15, null=True, blank=True)
    image = models.ImageField(verbose_name='Фото', upload_to='users', null=True, blank=True)
    passport = models.CharField(verbose_name='Паспорт', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


#### signal receiver. when User changed or created, Profile also updated or created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Permission(models.Model):
    code_name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    cr_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cr_on = models.DateTimeField(auto_now_add=True)
    up_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='permission_updated_by')
    up_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code_name


class Role(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    cr_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userrole_created_by', null=True, blank=True)
    cr_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.role.title)


class PermissionRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    grant = models.BooleanField(default=True)
    cr_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cr_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} {}'.format(self.role.title, self.permission.title, self.grant)


class PermissionUser(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grant = models.BooleanField(default=False)
    cr_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissionuser_created_by', null=True, blank=True)
    cr_on = models.DateTimeField(auto_now_add=True)


class ClientPhysical(models.Model):
    firstname = models.CharField(verbose_name="Имя", max_length=50)
    lastname = models.CharField(verbose_name="Фамилия", max_length=50)
    middlename = models.CharField(verbose_name="Отчество", max_length=50)
