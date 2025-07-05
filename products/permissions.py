from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):
    """
    Custom permission to only allow admins and managers to perform write operations.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin and manager
        return request.user.role in ['admin', 'manager']

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission for manager and admin roles.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'manager']
        )