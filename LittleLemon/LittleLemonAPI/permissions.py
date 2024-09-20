from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Manager').exists():
            return True


class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Delivery crew').exists():
            return True


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name="Delivery crew").exists() and not request.user.groups.filter(name='Manager').exists():
            return True
