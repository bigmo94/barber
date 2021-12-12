from rest_framework.permissions import BasePermission


class IsActivated(BasePermission):
    """
    Allows access only to active users.
    """

    def has_permission(self, request, view):
        flag = True
        if not (request.user and request.user.is_active):
            flag = False
        return flag


class IsOwner(BasePermission):
    """
    Allows access only to profile owner
    """

    def has_permission(self, request, view):
        flag = True
        if not (request.user and request.user == view.get_object()):
            flag = False
        return flag
