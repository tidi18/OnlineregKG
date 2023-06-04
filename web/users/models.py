from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=False)
    photo = models.ImageField(upload_to='user_photo', null=True)

    def suspend(self):
        self.status = User.STATUS_SUSPENDED
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Доп-инфа пользователей'
        verbose_name_plural = 'Доп-инфа пользователя'




