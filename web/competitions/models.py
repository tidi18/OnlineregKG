from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Competition(models.Model):
    hostState_list = [
        ('Кыргызстан', 'Кыргызстан'),
    ]

    region_list = [
        ('Бишкек', 'Бишкек'),
        ('Чуй', 'Чуй'),
        ('Каракол', 'Каракол'),
        ('Баткен', 'Баткен'),
        ('Джалал-Абад', 'Джалал-Абад'),
        ('Нарын', 'Нарын'),
        ('Талас', 'Талас'),
        ('Ош', 'Ош'),
    ]

    age_groups_of_participants_list = [
        ('до 18', 'до 18'),
        ('18-25', '18-25'),
        ('25-35', '25-35'),
        ('35-45', '35-45'),
        ('A, B, C, D', 'A, B, C, D ')
    ]

    phone_regex = RegexValidator(
        regex=r'\+996\d{9}$',
        message='Номер телефона должен быть в формате: "+996XXXXXXXXX'
    )
    telegram_regex = RegexValidator(
        regex=r'^@[A-Za-z0-9]{5,}$',
        message='invalid username Telegram'

    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitions', verbose_name='Редактор', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=hostState_list, max_length=10, blank=False, verbose_name='Государство проведения')
    region = models.CharField(choices=region_list, max_length=11, blank=False, verbose_name='Регион проведения')
    date = models.DateField(blank=False, verbose_name='Дата (-ы) проведения')
    organizer_name = models.CharField(max_length=30, blank=False,verbose_name='Имя организатора', null=True)
    organizer_last_name = models.CharField(max_length=100, blank=False, verbose_name='Фамилия организатора', null=True)
    organizer_email = models.EmailField(blank=False, verbose_name='email организатора', null=True)
    organizer_phone = models.CharField(max_length=13, blank=True, verbose_name='номер телефона организатора', null=True, validators=[phone_regex])
    organizer_telegram = models.CharField(max_length=20, blank=False, null=True, validators=[telegram_regex], verbose_name='Telegram организатора')
    organizer_whatsapp = models.CharField(max_length=255, blank=True, null=True, validators=[phone_regex], verbose_name='WhatsApp организатора')
    competition_name = models.CharField(max_length=255, blank=False, verbose_name='Наименование')
    location = models.CharField(max_length=255, blank=False, verbose_name='Место проведения')
    age_groups_of_participants = models.CharField(max_length=255, blank=False, verbose_name='Возрастные группы участников')
    illustration = models.ImageField(upload_to='competitions_illustration', blank=False, verbose_name='Иллюстрация')
    announcement = models.TextField(blank=False, verbose_name='Краткий анонс')
    coordinates_to_competition = models.CharField(max_length=255, blank=True, verbose_name='Точные координаты')
    slug = models.SlugField(unique=True, max_length=255)

    def set_age_groups(self, age_groups):
        self.age_groups_of_participants = ','.join(age_groups)

    def get_age_groups(self):
        return self.age_groups_of_participants.split(',')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.competition_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.competition_name

    def get_absolute_url(self):
        return reverse('competition_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'


def slugify_competitions_name(sender, instance, **kwargs):
    instance.slug = slugify(instance.competitions_name)
    models.signals.pre_save.connect(slugify_competitions_name, sender=Competition)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='comments',  blank=True, verbose_name='Соревнование')
    text = models.TextField(verbose_name='Сообщение')
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} ({self.competition})'

    class Meta:
        verbose_name = 'Комментарий '
        verbose_name_plural = 'Комментарии'


