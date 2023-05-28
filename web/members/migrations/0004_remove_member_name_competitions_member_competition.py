# Generated by Django 4.2 on 2023-05-08 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0008_competition_coordinates_to_competition_and_more'),
        ('members', '0003_alter_member_date_of_birth_alter_member_discharge_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='name_competitions',
        ),
        migrations.AddField(
            model_name='member',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='competitions.competition', verbose_name='Название соревнования'),
        ),
    ]
