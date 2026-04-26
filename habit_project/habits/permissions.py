from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пользователь может редактировать только свои привычки"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsPublicHabit(permissions.BasePermission):
    """Доступ только к публичным привычкам"""

    def has_permission(self, request, view):
        if view.action == 'list_public':
            return True
        return request.user.is_authenticated