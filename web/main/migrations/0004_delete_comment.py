# Generated by Django 4.2 on 2023-05-09 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_comment_author_alter_comment_competition_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
