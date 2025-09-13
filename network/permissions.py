from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Кастомный разрешение активного пользователя.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
