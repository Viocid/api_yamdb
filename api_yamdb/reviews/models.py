from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Title(models.Model):
    pass


def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError('Оценка должна быть от 1 до 10.')


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Оценка', validators=[validate_score])
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ('pub_date',)
        unique_together = ("author", "title")


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ('pub_date',)
