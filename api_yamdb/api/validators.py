from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError("Оценка должна быть от 1 до 10.")

def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError("Год указан неверно.")
