from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

class LoginView(LoginView):
    template_name = 'custom_auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Administrador').exists():
                return reverse_lazy('inventario:admin_dashboard')
            elif user.groups.filter(name='Gerente General').exists():
                return reverse_lazy('inventario:gerente_general_dashboard')
            elif user.groups.filter(name='Gerente').exists():
                return reverse_lazy('inventario:gerente_dashboard')
            elif user.groups.filter(name='Subgerente').exists():
                return reverse_lazy('inventario:subgerente_dashboard')
            elif user.groups.filter(name='Jefe').exists():
                return reverse_lazy('inventario:jefe_dashboard')
            elif user.groups.filter(name='Cliente').exists():
                return reverse_lazy('inventario:cliente_dashboard')
            elif user.groups.filter(name='Agente').exists():
                return reverse_lazy('inventario:agente_dashboard')
            return reverse_lazy('admin:index')  # Fallback
        return reverse_lazy('custom_auth:login')

@method_decorator(never_cache, name='dispatch')
class LogoutView(LogoutView):
    template_name = 'custom_auth/logout.html'
    next_page = reverse_lazy('custom_auth:login')