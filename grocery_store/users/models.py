from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from grocery_store.settings import MAX_LENGTH

from users.validators import validate_me


class User(AbstractUser):
    """ User Model """

    email = models.EmailField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='E-mail',
    )
    username = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        validators = (
            validate_me,
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='В имени пользователя можно использовать'
                        ' только буквы, цифры и символы "@/./+/-/_"!',
            ),
        ),
        verbose_name='Имя пользователя'
    )
    password = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Пароль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'id',
        )

    def __str__(self):
        return self.username
