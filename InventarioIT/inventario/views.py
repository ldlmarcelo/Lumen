from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ClienteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/cliente_dashboard.html'

class GerenteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/gerente_dashboard.html'

class AgenteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/agente_dashboard.html'

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/admin_dashboard.html'