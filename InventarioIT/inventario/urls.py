from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('cliente/', views.ClienteDashboardView.as_view(), name='cliente_dashboard'),
    path('jefe/', views.JefeDashboardView.as_view(), name='jefe_dashboard'),
    path('subgerente/', views.SubgerenteDashboardView.as_view(), name='subgerente_dashboard'),
    path('gerente/', views.GerenteDashboardView.as_view(), name='gerente_dashboard'),
    path('gerente_general/', views.GerenteGeneralDashboardView.as_view(), name='gerente_general_dashboard'),
    path('agente/', views.AgenteDashboardView.as_view(), name='agente_dashboard'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]