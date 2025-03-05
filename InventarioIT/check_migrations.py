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

# Verificar migraciones aplicadas en django_migrations
cursor.execute("SELECT app, name, applied FROM django_migrations ORDER BY app, applied")
rows = cursor.fetchall()

if rows:
    print("Migraciones aplicadas registradas en django_migrations:")
    for row in rows:
        app, name, applied = row
        print(f"App: {app}, Migration: {name}, Applied: {applied}")
else:
    print("No hay migraciones registradas en django_migrations.")

# Cerrar la conexión
conn.close()