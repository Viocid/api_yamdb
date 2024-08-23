from custom_users.constants import MAX_LENGHT_EMAIL, MAX_LENGHT_NAME
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ROLES = [(USER, "user"), (ADMIN, "admin"), (MODERATOR, "moderator")]

    username = models.CharField(
        max_length=MAX_LENGHT_NAME,
        unique=True,
        null=False,
        validators=[RegexValidator(r"^[\w.@+-]+\Z")],
    )
    email = models.EmailField(max_length=MAX_LENGHT_EMAIL, unique=True)
    first_name = models.CharField(max_length=MAX_LENGHT_NAME, blank=True)
    last_name = models.CharField(max_length=MAX_LENGHT_NAME, blank=True)
    bio = models.TextField(blank=True)
    role = models.SlugField(choices=ROLES, default=USER)
    confirmation_code = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

User = get_user_model()
