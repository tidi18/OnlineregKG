# Generated by Django 4.2 on 2023-04-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_member_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='date_of_birth',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='member',
            name='discharge',
            field=models.CharField(max_length=50, verbose_name='Разряд'),
        ),
        migrations.AlterField(
            model_name='member',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name_competitions',
            field=models.CharField(max_length=255, verbose_name='Название соревнования'),
        ),
        migrations.AlterField(
            model_name='member',
            name='team',
            field=models.CharField(blank=True, max_length=255, verbose_name='Команда'),
        ),
    ]
