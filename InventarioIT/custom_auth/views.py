from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class LoginView(LoginView):
    template_name = 'custom_auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Administrador').exists():
                return reverse_lazy('inventario:admin_dashboard')
            elif user.groups.filter(name='Gerente').exists():
                return reverse_lazy('inventario:gerente_dashboard')
            elif user.groups.filter(name='Agente').exists():
                return reverse_lazy('inventario:agente_dashboard')
            elif user.groups.filter(name='Cliente').exists():
                return reverse_lazy('inventario:cliente_dashboard')
            return reverse_lazy('admin:index')
        return reverse_lazy('custom_auth:login')

class LogoutView(LogoutView):
    next_page = reverse_lazy('custom_auth:login')