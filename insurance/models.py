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


class Product(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)


class Group(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)


class Klass(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)


class Bank(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)
    mfo = models.CharField(verbose_name="МФО банка", max_length=8)
    inn = models.CharField(verbose_name="ИНН", max_length=10)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
    checking_account = models.CharField(verbose_name="Расчётный счёт", max_length=30)


class Branch(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Currency(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=50)
    code = models.CharField(verbose_name="Код валюты", max_length=4)


class BasicTariffRate(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)
    sum = models.BigIntegerField(verbose_name="Сумма")


class Beneficiary(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)


class InsurancePeriod(models.Model):
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)


class LegalClient(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=255)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)


class IndividualClient(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)

#
# class CompanyBankAccount(models.Model):
#     bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
#     name = models.CharField(verbose_name="Наименование", max_length=255)
#     address = models.CharField(verbose_name="Адрес", max_length=150)
#     phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
#     checking_account = models.CharField(verbose_name="Расчётный счёт", max_length=30)
#
#
# class InsuranceContract(models.Model):
#     contract_number = models.IntegerField(verbose_name="Номер договора")  # TODO: make unsigned
#     contract_date = models.DateTimeField(verbose_name="Дата договора")  # TODO: discuss
#     # region = models.ForeignKey(Region, on_delete=models.SET_NULL)  TODO: fix
#     client_id = models.BigIntegerField()    # TODO: make unsigned
#     client_type = models.CharField(verbose_name="Тип клиента", max_length=1)
#     # client_checking_account = models.CharField(verbose_name="Расчётный счёт клиента", max_length=30)  TODO: discuss
#     # beneficiary = models.ForeignKey(Beneficiary, verbose_name="Выгодоприобретатель", on_delete=models.SET_NULL)  TODO: discuss
#     # pledger = models.ForeignKey(Pledger, verbose_name="Залогодатель", on_delete=models.SET_NULL)  TODO: discuss
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     loan_agreement = models.CharField(verbose_name="Кредитный договор", max_length=150)
#     property_name = models.CharField(verbose_name="Имя имущества", max_length=100)
#     quantity = models.IntegerField(verbose_name="Количество")  # TODO: discuss
#     insurance_cost = models.BigIntegerField(verbose_name="Страховая стоимость")  # TODO: discuss
#     insurance_sum = models.BigIntegerField(verbose_name="Страховая сумма")  # TODO: discuss
#     date_from = models.DateField()
#     date_to = models.DateField(null=True, blank=True)
#     franchise = models.CharField(verbose_name="Франшиза", max_length=100)
#     # installment_date = models.SmallIntegerField(verbose_name="Дата взносов")  TODO: discuss
#     original = models.TextField()  # TODO: change to Jsonb field
#
#
# class Policy(models.Model):
#     contract = models.ForeignKey(InsuranceContract, on_delete=models.SET_NULL, null=True, blank=True)
#     contract_number = models.IntegerField(verbose_name="Номер договора")  # TODO: make unsigned
#     property_name = models.CharField(verbose_name="Имя имущества", max_length=100)
#     # insurance_place = models.ForeignKey(Region, on_delete=models.SET_NULL)  TODO: fix
#     loan_agreement = models.CharField(verbose_name="Кредитный договор", max_length=150)
#     quantity = models.IntegerField(verbose_name="Количество")  # TODO: discuss
#     insurance_case = models.CharField(verbose_name="Страховой случае", max_length=100)
#     insurance_sum = models.BigIntegerField(verbose_name="Страховая сумма")  # TODO: discuss
#     franchise = models.CharField(verbose_name="Франшиза", max_length=100)
#     total_prize = models.BigIntegerField(verbose_name=" Общая страховая премия")  # TODO: discuss
#     paid_insurance_prize = models.BigIntegerField(verbose_name="Оплаченная страховая премия")  # TODO: discuss
#     date_from = models.DateField()
#     date_to = models.DateField(null=True, blank=True)
#     policy_date = models.DateField(verbose_name="Дата полиса")
#     issue_date = models.DateField(verbose_name="Дата выдачи")
#     # manager = models.ForeignKey(Beneficiary, verbose_name="Директор", on_delete=models.SET_NULL)  TODO: discuss
#     original = models.TextField()  # TODO: change to Jsonb field
#
#
# class Transaction(models.Model):
#     client_id = models.BigIntegerField()    # TODO: make unsigned
#     client_type = models.CharField(verbose_name="Тип клиента", max_length=1)
#     bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
#     sum = models.BigIntegerField(verbose_name="Сумма")
#     time = models.DateField(auto_now_add=True)
#     bank_checking_account = models.ForeignKey(CompanyBankAccount, verbose_name="Расчётный счёт", on_delete=models.SET_NULL, null=True, blank=True)
#     client_checking_account = models.CharField(verbose_name="Расчётный счёт клиента", max_length=30)
#     contract = models.ForeignKey(InsuranceContract, on_delete=models.SET_NULL, null=True, blank=True)
#     comments = models.TextField()   # TODO: discuss about jsonb
#
#
# class Form(models.Model):
#     # beneficiary = models.ForeignKey(Beneficiary, verbose_name="Выгодоприобретатель", on_delete=models.SET_NULL)  TODO: discuss
#     # form_type = models.ForeignKey(FormType)
#     date_from = models.DateField()
#     date_to = models.DateField(null=True, blank=True)
#     property_name = models.CharField(verbose_name="Имя имущества", max_length=100)
#     client_id = models.BigIntegerField()    # TODO: make unsigned
#     client_type = models.CharField(verbose_name="Тип клиента", max_length=1)
#     # client_checking_account = models.CharField(verbose_name="Расчётный счёт клиента", max_length=30)  TODO: discuss
#     # region = models.ForeignKey(Region, on_delete=models.SET_NULL)  TODO: fix
#     quantity = models.IntegerField(verbose_name="Количество")  # TODO: discuss
#     insurance_cost = models.BigIntegerField(verbose_name="Страховая стоимость")  # TODO: discuss
#     insurance_sum = models.BigIntegerField(verbose_name="Страховая сумма")  # TODO: discuss
#     anti_fire_stuff = models.SmallIntegerField(verbose_name="Наличие пожарной сигнализации и средств пожаротушения")
#     security_stuff = models.SmallIntegerField(verbose_name="Наличие охранной сигнализации и средств защиты")
#     payment_type = models.CharField(verbose_name="Вид оплаты", max_length=1)
#     payment_currency = models.CharField(verbose_name="Валюта оплаты", max_length=4)
#     insurer = models.ForeignKey(User, verbose_name="Страхователь", on_delete=models.SET_NULL, null=True, blank=True)


class Dt_Option(models.Model):
    codeName = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=512, null=True, blank=True)
    dataPath = models.CharField(max_length=512, null=True, blank=True)
    draw = models.IntegerField(default=1, null=True, blank=True)
    keys = models.BooleanField(default=True)
    colReorder = models.BooleanField(default=True)
    fixedHeader = models.BooleanField(default=True)
    responsive = models.BooleanField(default=True)
    autoFill = models.BooleanField(default=True)
    serverSide = models.BooleanField(default=True)
    processing = models.BooleanField(default=True)
    scrollY = models.CharField(max_length=128, default='70vh')

    def __str__(self):
        return self.codeName


class GridCols(models.Model):
    table = models.ForeignKey(Dt_Option, on_delete=models.CASCADE, related_name='columns', null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    data = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    type = models.CharField(max_length=128, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    searchable = models.BooleanField(default=True)
    orderable = models.BooleanField(default=True)
    className = models.CharField(max_length=128, null=True, blank=True)
    defaultContent = models.CharField(max_length=1024, null=True, blank=True)
    visible = models.BooleanField(default=True)
    order_num = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order_num']

    def __str__(self):
        return self.title
