from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gerencia = models.ForeignKey('inventario.Gerencia', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Gerencia")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.username