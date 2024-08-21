from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrAnyReadOnly(permissions.AllowAny):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            not request.user.is_anonymous and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором отзыва,
    либо имеет права администратора.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
