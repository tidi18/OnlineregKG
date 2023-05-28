# Generated by Django 4.2 on 2023-04-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0005_remove_competition_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
