# Generated by Django 4.2 on 2023-05-25 07:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0019_rename_name_competition_competition_competition_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='organizer_phone',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: "+996XXXXXXXXX', regex='\\+996\\d{9}$')], verbose_name='номер телефона организатора'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='organizer_telegram',
            field=models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='invalid username Telegram', regex='^@[A-Za-z0-9]{5,}$')], verbose_name='Telegram организатора'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='organizer_whatsapp',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: "+996XXXXXXXXX', regex='\\+996\\d{9}$')], verbose_name='WhatsApp организатора'),
        ),
    ]
