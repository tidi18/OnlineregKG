from django.db import models
from competitions.models import Competition


class Member(models.Model):

    discharge_list = [
        ('3 юношеский', '3 юношеский'),
        ('2 юношеский', '2 юношеский'),
        ('1 юношеский', '1 юношеский'),
        ('3 спортивный', '3 спортивный'),
        ('2 спортивный', '2 спортивный'),
        ('1 спортивный', '1 спортивный'),
        ('Кандидат в мастера спорта', 'Кандидат в мастера спорта'),
        ('Мастер спорта', 'Мастер спорта'),
        ('Заслуженный мастер спорта', 'Заслуженный мастер спорта'),
        ('Мастер спорта международного класса', 'Мастер спорта международного класса')

    ]

    competition = models.ForeignKey(Competition, related_name='members', blank=False, verbose_name='Название соревнования', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=False, verbose_name='Фамилия')
    discharge = models.CharField(max_length=50, blank=False, verbose_name='Разряд')
    team = models.CharField(max_length=255, blank=True, verbose_name='Команда')
    date_of_birth = models.DateField(blank=False, verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.competition} {self.name} {self.last_name}'

    class Meta:
        verbose_name = 'Участника'
        verbose_name_plural = 'Участники'

