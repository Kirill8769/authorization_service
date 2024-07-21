from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """Проверяет, является ли пользователь пользователем."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
