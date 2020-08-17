# Generated by Django 2.2.6 on 2020-08-14 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0004_gridcols_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dt_Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeName', models.CharField(max_length=128, unique=True)),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('dataPath', models.CharField(blank=True, max_length=512, null=True)),
                ('draw', models.IntegerField(blank=True, default=1, null=True)),
                ('keys', models.BooleanField(default=True)),
                ('colReorder', models.BooleanField(default=True)),
                ('fixedHeader', models.BooleanField(default=True)),
                ('responsive', models.BooleanField(default=True)),
                ('autoFill', models.BooleanField(default=True)),
                ('serverSide', models.BooleanField(default=True)),
                ('processing', models.BooleanField(default=True)),
                ('scrollY', models.CharField(default='70vh', max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='gridcols',
            name='grid',
        ),
        migrations.RemoveField(
            model_name='gridcols',
            name='maxWidth',
        ),
        migrations.DeleteModel(
            name='Grid',
        ),
        migrations.AddField(
            model_name='gridcols',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='column_table', to='insurance.Dt_Option'),
        ),
    ]