# Generated by Django 4.2 on 2023-05-24 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0016_alter_competition_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='create_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
