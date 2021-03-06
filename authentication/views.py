from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

    def get_success_url(self):
        return reverse_lazy('articles')


class CustomLogoutView(LogoutView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
