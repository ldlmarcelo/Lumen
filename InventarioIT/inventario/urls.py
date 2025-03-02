from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('cliente/', views.ClienteDashboardView.as_view(), name='cliente_dashboard'),
    path('gerente/', views.GerenteDashboardView.as_view(), name='gerente_dashboard'),
    path('agente/', views.AgenteDashboardView.as_view(), name='agente_dashboard'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]