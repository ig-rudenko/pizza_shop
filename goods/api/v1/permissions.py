from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOrderOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.id in request.session.get("orders"):
            # Если заказ, который мы хотим посмотреть находится в списке наших,
            # то можно с ним работать
            return True
        # Нельзя
        return False
