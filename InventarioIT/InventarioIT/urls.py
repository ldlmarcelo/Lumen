from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('inventario/', include('inventario.urls')),
]