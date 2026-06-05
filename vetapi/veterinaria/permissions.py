from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """Staff escribe o altera ítems clínicos, clientes solo leen."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and (request.user.is_staff or request.user.role == 'VET'))

class IsOwnerOrStaff(BasePermission):
    """El dueño del ticket puede verlo, los veterinarios o admins pueden mutarlo."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or request.user.role == 'VET'