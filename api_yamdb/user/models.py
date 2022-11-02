from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True,
    )
    email = models.EmailField(verbose_name='Email',
                              unique=True,
                              )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
    )
    bio = models.TextField(
        verbose_name='Роль',
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]
