from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dispositivo, DispositivoUbicacion, DispositivoEstado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Dispositivo, DispositivoCaracteristica, DispositivoEstado, DispositivoUbicacion, DispositivoPropietarioHistorico, TipoDispositivo
from .forms import DispositivoForm, DispositivoCaracteristicaForm, DispositivoEstadoForm, DispositivoUbicacionForm, DispositivoPropietarioHistoricoForm
from django.contrib.auth.models import Group



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

        # Decorador para verificar rol Agente
# Decorador para verificar rol Agente
def is_agente(user):
    return user.is_authenticated and user.groups.filter(name='Agente').exists()

# Vista para listar dispositivos
@login_required
@user_passes_test(is_agente)
def lista_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, 'inventario/agente/lista_dispositivos.html', {'dispositivos': dispositivos})

# Vista para crear un dispositivo
@login_required
@user_passes_test(is_agente)
def crear_dispositivo(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            dispositivo = form.save()
            messages.success(request, 'Dispositivo creado exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm()
    return render(request, 'inventario/agente/crear_dispositivo.html', {'form': form})

# Vista para editar un dispositivo
@login_required
@user_passes_test(is_agente)
def editar_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo actualizado exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'inventario/agente/editar_dispositivo.html', {'form': form, 'dispositivo': dispositivo})

# Vista para eliminar un dispositivo
@login_required
@user_passes_test(is_agente)
def eliminar_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    if request.method == 'POST':
        dispositivo.delete()
        messages.success(request, 'Dispositivo eliminado exitosamente.')
        return redirect('lista_dispositivos')
    return render(request, 'inventario/agente/confirmar_eliminar_dispositivo.html', {'dispositivo': dispositivo})

# Vista para crear una característica de dispositivo
@login_required
@user_passes_test(is_agente)
def crear_caracteristica(request):
    if request.method == 'POST':
        form = DispositivoCaracteristicaForm(request.POST)
        if form.is_valid():
            caracteristica = form.save(commit=False)
            # Validar procesador obligatorio para dispositivos tipo "De cómputo"
            if caracteristica.dispositivo.subtipo_dispositivo.tipo_dispositivo.nombre == "De cómputo":
                if not caracteristica.procesador and not (caracteristica.caracteristica and caracteristica.caracteristica.nombre == "Procesador"):
                    return JsonResponse({'error': 'No se ha asignado un procesador al equipo. ¿Aceptar/Cancelar?'}, status=400)
            caracteristica.save()
            messages.success(request, 'Característica creada exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoCaracteristicaForm()
    return render(request, 'inventario/agente/crear_caracteristica.html', {'form': form})

# Vista para crear un estado de dispositivo
@login_required
@user_passes_test(is_agente)
def crear_estado(request):
    if request.method == 'POST':
        form = DispositivoEstadoForm(request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            estado.agente = request.user
            estado.save()
            messages.success(request, 'Estado creado exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoEstadoForm()
    return render(request, 'inventario/agente/crear_estado.html', {'form': form})

# Vista para crear una ubicación de dispositivo
@login_required
@user_passes_test(is_agente)
def crear_ubicacion(request):
    if request.method == 'POST':
        form = DispositivoUbicacionForm(request.POST)
        if form.is_valid():
            ubicacion = form.save(commit=False)
            ubicacion.agente = request.user
            ubicacion.save()
            messages.success(request, 'Ubicación creada exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoUbicacionForm()
    return render(request, 'inventario/agente/crear_ubicacion.html', {'form': form})

# Vista para crear un cambio de propietario de dispositivo
@login_required
@user_passes_test(is_agente)
def crear_propietario_historico(request):
    if request.method == 'POST':
        form = DispositivoPropietarioHistoricoForm(request.POST)
        if form.is_valid():
            historico = form.save(commit=False)
            historico.agente = request.user
            historico.save()
            messages.success(request, 'Cambio de propietario creado exitosamente.')
            return redirect('lista_dispositivos')
    else:
        form = DispositivoPropietarioHistoricoForm()
    return render(request, 'inventario/agente/crear_propietario_historico.html', {'form': form})