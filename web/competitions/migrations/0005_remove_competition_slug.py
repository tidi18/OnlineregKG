# Generated by Django 4.2 on 2023-04-24 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0004_competition_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='slug',
        ),
    ]