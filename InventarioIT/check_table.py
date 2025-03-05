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

# Lista de apps y sus modelos para verificar
apps_to_check = [
    'custom_auth',
    'inventario',
]

# Obtener todas las tablas de las apps especificadas
for app in apps_to_check:
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{app}_%'")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"{table_name}: {count} registros")

# Cerrar la conexión
conn.close()