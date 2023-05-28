from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    email = models.EmailField(max_length=100, blank=False)
    subject = models.CharField(max_length=100, blank=False, verbose_name='Тема')
    message = models.TextField(max_length=500, blank=False, verbose_name='Сообщение')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'







