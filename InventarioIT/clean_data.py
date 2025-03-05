import os
import django
import sqlite3

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIT.settings')
django.setup()

from django.conf import settings

# Conectar a la base de datos SQLite
conn = sqlite3.connect(settings.DATABASES['default']['NAME'])  # 'db.sqlite3'
cursor = conn.cursor()

# Lista de tablas de custom_auth e inventario, en orden inverso de dependencias
tables_to_clean = [
    # Tablas de inventario (orden inverso de dependencias)
    'inventario_dispositivopropietariohistorico',
    'inventario_dispositivoubicacion',
    'inventario_dispositivoestado',
    'inventario_dispositivocaracteristica',
    'inventario_caracteristicatipodispositivo',
    'inventario_dispositivo',
    'inventario_procesador',
    'inventario_modelo',
    'inventario_ubicacion',
    'inventario_estadodispositivo',
    'inventario_subtipodispositivo',
    'inventario_tipodispositivo',
    'inventario_caracteristica',
    'inventario_cantidadmemoria',
    'inventario_tipomemoria',
    'inventario_marca',
    'inventario_gerencia',
    # Tablas de custom_auth (orden inverso de dependencias)
    'custom_auth_customuser_user_permissions',
    'custom_auth_customuser_groups',
    'custom_auth_customuser',
]

# Limpiar cada tabla
for table in tables_to_clean:
    try:
        cursor.execute(f"DELETE FROM {table}")
        print(f"Limpios {cursor.rowcount} registros de {table}")
    except sqlite3.OperationalError as e:
        print(f"Error al limpiar {table}: {e}")

# Confirmar los cambios en la base de datos
conn.commit()
print("Base de datos limpiada exitosamente.")

# Cerrar la conexión
conn.close()