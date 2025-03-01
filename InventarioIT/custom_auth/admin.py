from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'gerencia', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gerencia',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)