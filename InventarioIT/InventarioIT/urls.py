from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('inventario/', include('inventario.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/auth/login/'), name='logout'),  # Nueva ruta para logout
]