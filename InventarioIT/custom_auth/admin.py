from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'get_gerencia', 'is_staff']  # Cambiar 'gerencia' por 'get_gerencia'
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gerencia',)}),  # Mantener gerencia en fieldsets
    )

    def get_gerencia(self, obj):
        return obj.gerencia.nombre if obj.gerencia else "Sin gerencia"
    get_gerencia.short_description = "Gerencia"  # Nombre en la columna del admin

admin.site.register(CustomUser, CustomUserAdmin)