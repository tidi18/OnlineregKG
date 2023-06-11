# Generated by Django 4.2 on 2023-05-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usergroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='can_add_comments',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='can_view_pages',
            field=models.BooleanField(default=False),
        ),
    ]