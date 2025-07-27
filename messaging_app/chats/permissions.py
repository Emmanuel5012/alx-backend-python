from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
    