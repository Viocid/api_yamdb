from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from .constants import (
    MAX_NAME_LENGTH,
    MAX_SLUG_LENGTH
)


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        'Категория',
        max_length=MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        'Идентификатор категории',
        unique=True,
        max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField(
        'Жанр',
        max_length=MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        'Идентификатор жанра',
        unique=True,
        max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        'Произведение',
        max_length=MAX_NAME_LENGTH
    )
    year = models.IntegerField(
        'Год выпуска'
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreToTitle',
        verbose_name='Жанр'
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(year__lte=timezone.now().year),
                name='check_year',
            ),
        ]
        ordering = ('name',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Присвоение жанров произведениям."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title}, {self.genre}'
