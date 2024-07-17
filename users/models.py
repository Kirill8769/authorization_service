from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=12, unique=True, verbose_name='Телефон')
    my_invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True, verbose_name='Мой инвайт-код')
    another_invite_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='Чужой инвайт-код')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ('pk', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
