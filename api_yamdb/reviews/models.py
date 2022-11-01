from enum import unique
from tabnanny import verbose
from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name


class Ganre(models.Model):
    name = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        help_text='Укажите год',
        verbose_name='Год релиза'
    )

    genre = models.ManyToManyField(
        'Жанр',
        through='GenreTitle',
        verbose_name='Жанр'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self) -> str:
        return self.name
