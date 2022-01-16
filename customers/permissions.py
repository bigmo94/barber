from rest_framework.permissions import BasePermission


class IsEnabled(BasePermission):
    """
    Allows access only to active users.
    """

    def has_permission(self, request, view):
        flag = True
        if not (request.user and request.user.is_enable):
            flag = False
        return flag


class IsOwner(BasePermission):
    """
    Allows access only to profile owner
    """

    def has_permission(self, request, view):
        flag = True
        if not (request.user and request.user == view.get_object() or request.user == view.get_object().user):
            flag = False
        return flag


class IsEmployee(BasePermission):
    """
    Allows access only to employee
    """

    def has_permission(self, request, view):
        flag = True
        if not (request.user and request.user.is_employee):
            flag = False
        return flag
