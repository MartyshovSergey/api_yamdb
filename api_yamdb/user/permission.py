from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Если не Администратор, только права на чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and (
                        request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """Если не Администратор, Модератора, Владелец, только права на чтение."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(BasePermission):
    """Суперюзер Django — обладает правами администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser)
