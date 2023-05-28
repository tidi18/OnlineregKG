from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', verbose_name='Автор')
    date = models.DateField(auto_now=True, verbose_name='дата')
    header = models.CharField(max_length=255, blank=False, verbose_name='Заголовок', null=True)
    announcement = models.TextField(blank=False, verbose_name='Анонс', null=True)
    photo = models.ImageField(upload_to='news_photo', blank=False, verbose_name='Фото', null=True)
    text = models.TextField(blank=False, verbose_name='Текст', null=True)
    slug = models.SlugField(unique=True, max_length=255, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.header)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


def slugify_news_header(sender, instance, **kwargs):
    instance.slug = slugify(instance.header)
    models.signals.pre_save.connect(slugify_news_header, sender=News)


