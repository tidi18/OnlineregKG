# Generated by Django 4.2 on 2023-05-09 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitions', '0008_competition_coordinates_to_competition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='illustration',
            field=models.ImageField(upload_to='competitions_illustration', verbose_name='Иллюстрация'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Сообщение')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('competition', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='competitions.competition', verbose_name='Соревнование')),
            ],
            options={
                'verbose_name': 'Комментарий ',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
