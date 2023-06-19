from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class IsExpiringLinkCreate(IsAuthenticated):
    def has_permission(self, request, view):
        is_expiring_link = request.user.account.plan.is_expiring_link
        if not is_expiring_link:
            raise PermissionDenied('You can not create expiring links to images on your current plan.')
        return is_expiring_link
