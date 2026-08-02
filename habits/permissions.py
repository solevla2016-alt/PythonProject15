from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Владелец может редактировать/удалять свою привычку.
    Остальные могут только читать публичные привычки.
    """

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Только владелец может редактировать/удалять
        return obj.user == request.user
