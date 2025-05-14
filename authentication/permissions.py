from rest_framework.permissions import BasePermission

class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'investor'


class IsOrganisation(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'organisation'

class IsInvestorOrOrganisation(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.account_type == 'investor' or
            request.user.account_type == 'organisation'
        )
    
class IsPersonal(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'personal'