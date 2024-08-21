from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrAnyReadOnly(permissions.AllowAny):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_admin
        )
