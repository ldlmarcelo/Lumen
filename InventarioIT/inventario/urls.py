from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Dashboards por rol (manteniendo las vistas basadas en clases)
    path('cliente/', views.ClienteDashboardView.as_view(), name='cliente_dashboard'),
    path('jefe/', views.JefeDashboardView.as_view(), name='jefe_dashboard'),
    path('subgerente/', views.SubgerenteDashboardView.as_view(), name='subgerente_dashboard'),
    path('gerente/', views.GerenteDashboardView.as_view(), name='gerente_dashboard'),
    path('gerente_general/', views.GerenteGeneralDashboardView.as_view(), name='gerente_general_dashboard'),
    path('agente/', views.AgenteDashboardView.as_view(), name='agente_dashboard'),  # Dashboard genérico del agente
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # CRUD de dispositivos (manteniendo las vistas basadas en funciones)
    path('', views.lista_dispositivos, name='lista_dispositivos'),
    path('crear/', views.crear_dispositivo, name='crear_dispositivo'),
    path('editar/<int:pk>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('eliminar/<int:pk>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('crear_caracteristica/', views.crear_caracteristica, name='crear_caracteristica'),
    path('crear_estado/', views.crear_estado, name='crear_estado'),
    path('crear_ubicacion/', views.crear_ubicacion, name='crear_ubicacion'),
    path('crear_propietario_historico/', views.crear_propietario_historico, name='crear_propietario_historico'),
]