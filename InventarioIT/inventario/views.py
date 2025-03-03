from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dispositivo, DispositivoUbicacion, DispositivoEstado

class ClienteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/cliente_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        dispositivos = Dispositivo.objects.filter(propietario=user, is_active=True)
        for dispositivo in dispositivos:
            dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
            dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
        context['dispositivos'] = dispositivos
        return context

class JefeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/jefe_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        if user.gerencia:
            ramas = user.gerencia.get_descendants(include_self=True)
            dispositivos = Dispositivo.objects.filter(propietario__gerencia__in=ramas, is_active=True)
            for dispositivo in dispositivos:
                dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
                dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
            context['dispositivos'] = dispositivos
        return context

class SubgerenteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/subgerente_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        if user.gerencia:
            ramas = user.gerencia.get_descendants(include_self=True)
            dispositivos = Dispositivo.objects.filter(propietario__gerencia__in=ramas, is_active=True)
            for dispositivo in dispositivos:
                dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
                dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
            context['dispositivos'] = dispositivos
        return context

class GerenteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/gerente_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        if user.gerencia:
            ramas = user.gerencia.get_descendants(include_self=True)
            dispositivos = Dispositivo.objects.filter(propietario__gerencia__in=ramas, is_active=True)
            for dispositivo in dispositivos:
                dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
                dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                    dispositivo_id_dispositivo=dispositivo, is_active=True
                ).order_by('-fecha').first()
            context['dispositivos'] = dispositivos
        return context

class GerenteGeneralDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/gerente_general_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        dispositivos = Dispositivo.objects.filter(is_active=True)  # Ve todo
        for dispositivo in dispositivos:
            dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
            dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
        context['dispositivos'] = dispositivos
        return context

class AgenteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/agente_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        dispositivos = Dispositivo.objects.all()
        for dispositivo in dispositivos:
            dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
            dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
        context['dispositivos'] = dispositivos
        return context

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['gerencia_usuario'] = user.gerencia
        dispositivos = Dispositivo.objects.all()
        for dispositivo in dispositivos:
            dispositivo.ultima_ubicacion = DispositivoUbicacion.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
            dispositivo.ultimo_estado = DispositivoEstado.objects.filter(
                dispositivo_id_dispositivo=dispositivo, is_active=True
            ).order_by('-fecha').first()
        context['dispositivos'] = dispositivos
        return context