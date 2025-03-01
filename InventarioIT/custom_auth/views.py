from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class LoginView(LoginView):
    template_name = 'custom_auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            # Temporalmente, redirigimos a una página genérica o admin
            return reverse_lazy('admin:index')  # Panel de admin como fallback
        return reverse_lazy('custom_auth:login')  # Fallback si no autenticado

class LogoutView(LogoutView):
    next_page = reverse_lazy('custom_auth:login')