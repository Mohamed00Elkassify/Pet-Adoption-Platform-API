from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Purpose:

    Anyone can read the object (GET, HEAD, OPTIONS).

    Only the owner of the object can edit/delete it (PUT, PATCH, DELETE).

    Used for:

    Objects that have an owner field — like Pet model.

    Example: If Alice owns a pet, she can update or delete it. Bob can only view it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class IsPetOwner(permissions.BasePermission):
    """
    Purpose:
    
    Only the owner of the pet related to the object can access it.
    
    Used for:
    
    Objects that are related to a pet, like AdoptionRequest.
    
    Example: If Alice owns a pet, she can view adoption requests for that pet. Bob cannot.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming obj is an AdoptionRequest instance
        return obj.pet.owner == request.user
