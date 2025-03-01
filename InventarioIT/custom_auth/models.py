from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gerencia = models.ForeignKey(
        'inventario.Gerencia',  # Referencia cruzada a la app inventario
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Gerencia"
    )

    def __str__(self):
        return self.username