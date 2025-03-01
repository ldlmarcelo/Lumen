from django.contrib import admin
from .models import (
    Gerencia, TipoDispositivo, EstadoDispositivo, Ubicacion, Marca, Modelo,
    Caracteristica, CantidadMemoria, TipoMemoria, CaracteristicaEspecifica,
    Dispositivo, DispositivoCaracteristica, DispositivoEstado,
    DispositivoUbicacion, DispositivoPropietarioHistorico
)

# Registro simple para todos los modelos
admin.site.register(Gerencia)
admin.site.register(TipoDispositivo)
admin.site.register(EstadoDispositivo)
admin.site.register(Ubicacion)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Caracteristica)
admin.site.register(CantidadMemoria)
admin.site.register(TipoMemoria)
admin.site.register(CaracteristicaEspecifica)
admin.site.register(Dispositivo)
admin.site.register(DispositivoCaracteristica)
admin.site.register(DispositivoEstado)
admin.site.register(DispositivoUbicacion)
admin.site.register(DispositivoPropietarioHistorico)