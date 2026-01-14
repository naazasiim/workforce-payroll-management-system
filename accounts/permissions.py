from rest_framework.permissions import BasePermission


class IsHRorManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.role in ["HR", "MANAGER"]
        )
