# Generated by Django 4.2.2 on 2023-06-26 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0023_alter_competition_age_groups_of_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='age_groups_of_participants',
            field=models.TextField(verbose_name='Возрастные группы участников'),
        ),
    ]
