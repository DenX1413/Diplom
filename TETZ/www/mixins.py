from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки авторизации с кастомным сообщением"""
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Для доступа к этой странице необходимо авторизоваться')
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

