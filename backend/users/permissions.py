from rest_framework.permissions import SAFE_METHODS, BasePermission


class ProduceOwnerPermission(BasePermission):
    message = 'Managing this product is restricted to the publisher/owner only.'

    def has_object_permission(self, request, view, obj):
        if request.methond in SAFE_METHODS:
            return True

        return obj.User == request.user
