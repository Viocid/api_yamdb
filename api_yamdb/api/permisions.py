from rest_framework import permissions


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
