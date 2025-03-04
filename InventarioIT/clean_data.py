import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIT.settings')
django.setup()

from django.apps import apps

# Lista de modelos a limpiar (ajusta según necesites, quitando SubtipoDispositivo)
models_to_clear = [
    'custom_auth.customuser',
    'inventario.gerencia',
    'inventario.tipodispositivo',
    'inventario.estadodispositivo',
    'inventario.ubicacion',
    'inventario.marca',
    'inventario.modelo',
    'inventario.caracteristica',
    'inventario.caracteristicatipodispositivo',
    'inventario.dispositivo',
    'inventario.dispositivocaracteristica',
    'inventario.dispositivoubicacion',
    'inventario.dispositivoestado',
    'inventario.dispositivopropietariohistorico',
    'inventario.tipoMemoria',
    'inventario.cantidadMemoria',
]

for model_name in models_to_clear:
    try:
        model = apps.get_model(model_name)
        model.objects.all().delete()
        print(f"Limpiados datos de {model_name}")
    except Exception as e:
        print(f"Error limpiando {model_name}: {e}")

print("Datos limpiados exitosamente.")