from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_customer
