from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from reviews.constants import (
    MAX_NAME_LENGTH,
    MAX_SLUG_LENGTH,
    REVIEW_TEXT_CUT,
    COMMENT_TEXT_CUT,
)
from reviews.validators import validate_score, validate_year

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField("Категория", max_length=MAX_NAME_LENGTH)
    slug = models.SlugField(
        "Идентификатор категории", unique=True, max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        ordering = ("slug",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField("Жанр", max_length=MAX_NAME_LENGTH)
    slug = models.SlugField(
        "Идентификатор жанра", unique=True, max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        ordering = ("slug",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField("Произведение", max_length=MAX_NAME_LENGTH)
    year = models.SmallIntegerField("Год выпуска", validators=[validate_year])
    description = models.TextField("Описание", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre, through="GenreToTitle", verbose_name="Жанр"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(year__lte=timezone.now().year),
                name="check_year",
            ),
        ]
        ordering = ("name",)
        default_related_name = "titles"
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Присвоение жанров произведениям."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение", null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="Жанр", null=True
    )

    class Meta:
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведений"

    def __str__(self):
        return f"{self.title}, {self.genre}"


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        "Оценка", validators=[validate_score]
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:REVIEW_TEXT_CUT]

    class Meta:
        ordering = ("pub_date",)
        unique_together = ("author", "title")


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:COMMENT_TEXT_CUT]

    class Meta:
        ordering = ("pub_date",)
