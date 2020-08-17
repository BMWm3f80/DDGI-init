# Generated by Django 2.2.6 on 2020-08-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('middle_name', models.CharField(max_length=255, verbose_name='Отчество')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
            ],
        ),
    ]