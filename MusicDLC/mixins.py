from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.user.is_superuser:
            messages.error(request, 'Necesitas ser un Administrador para entrar!')
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super().dispatch(request, *args, **kwargs)

class UserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_superuser