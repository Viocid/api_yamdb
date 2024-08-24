from django.core.validators import MaxLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from custom_users.constants import MAX_LENGTH_EMAIL
from custom_users.models import CustomUser
from custom_users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для эндпоинта 'users/me/' для любого авторизов. пользователя.
    [GET] персональные данные пользователя.
    [POST] заполнение полей 'first_name', 'last_name' и 'bio'.
    """

    role = serializers.StringRelatedField(read_only=True)
    username = serializers.RegexField(
        r"^[\w.@+-]{1,150}$",
    )
    email = serializers.EmailField(
        validators=[MaxLengthValidator(MAX_LENGTH_EMAIL)]
    )

    class Meta:
        model = CustomUser
        ordering = ["id"]
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserAdminSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для эндпоинта 'users/' для пользователя с ролью 'admin'.
    [GET] получение списка пользователей.
    [POST] регистрация нового пользователя.
    [GET, PATCH, DELETE] работа с пользователем по username.
    """

    class Meta:
        model = CustomUser
        ordering = ["id"]
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate(self, data):
        if self.initial_data.get("username") == "me":
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "confirmation_code")


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username, UnicodeUsernameValidator()),
    )

    def validate(self, data):
        try:
            CustomUser.objects.get_or_create(
                username=data.get("username"), email=data.get("email")
            )
        except IntegrityError:
            raise serializers.ValidationError(
                "Одно из полей username или email уже занято"
            )
        return data
