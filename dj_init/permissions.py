"""
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from rest_framework import permissions

User = get_user_model()


def is_superuser(user):
    return user.is_superuser


class IsVerifiedPermission(permissions.BasePermission):
    message = 'You profile is not verified or inactive to access the API.'

    def has_permission(self, request, view):
        if request.user.is_active_user():
            return True
        return False


class AdminPermissionMixin(View):
    @method_decorator(login_required(login_url=reverse_lazy('web:admin-web-login')))
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return super(AdminPermissionMixin, self).dispatch(*args, **kwargs)
        raise PermissionDenied
