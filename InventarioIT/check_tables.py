import os
import sqlite3
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIT.settings')
django.setup()

from django.conf import settings

# Conectar a la base de datos SQLite
conn = sqlite3.connect(settings.DATABASES['default']['NAME'])  # 'db.sqlite3'
cursor = conn.cursor()

# Obtener todas las tablas en la base
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Verificar el conteo de registros en cada tabla
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT count(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Tabla {table_name}: {count} registros")

# Cerrar la conexión
conn.close()