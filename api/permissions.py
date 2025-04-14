from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        return (obj.by == request.user) or request.user.is_superuser or request.user.is_staff


class AdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and bool(request.user.is_staff or request.user.is_superuser)


class NotAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
