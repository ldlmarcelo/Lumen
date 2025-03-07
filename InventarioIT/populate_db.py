import datetime
from django.db import transaction
from django.contrib.auth.hashers import make_password
from custom_auth.models import CustomUser
from inventario.models import (
    Gerencia, TipoDispositivo, SubtipoDispositivo, Caracteristica,
    CaracteristicaTipoDispositivo, EstadoDispositivo, Ubicacion, Marca,
    Modelo, CantidadMemoria, TipoMemoria, Procesador, Dispositivo,
    DispositivoCaracteristica, DispositivoEstado, DispositivoUbicacion,
    DispositivoPropietarioHistorico
)

@transaction.atomic
def populate_db():
    print("Poblando la base de datos...")

    # 1. Crear Gerencias (estructura jerárquica)
    gerencia_general = Gerencia.objects.create(nombre="Gerencia General", is_active=True)
    gerencia_it = Gerencia.objects.create(nombre="Gerencia IT", parent=gerencia_general, is_active=True)
    jefatura_redes = Gerencia.objects.create(nombre="Jefatura Redes", parent=gerencia_it, is_active=True)
    jefatura_soporte = Gerencia.objects.create(nombre="Jefatura Soporte", parent=gerencia_it, is_active=True)

    # 2. Crear usuarios con diferentes roles
    admin = CustomUser.objects.create(
        username="admin", password=make_password("admin123"), is_superuser=True, is_staff=True
    )
    gerente_general = CustomUser.objects.create(
        username="gerente_general", password=make_password("gerente123"), gerencia=gerencia_general
    )
    gerente_it = CustomUser.objects.create(
        username="gerente_it", password=make_password("gerenteit123"), gerencia=gerencia_it
    )
    subgerente_redes = CustomUser.objects.create(
        username="subgerente_redes", password=make_password("subgerente123"), gerencia=jefatura_redes
    )
    jefe_soporte = CustomUser.objects.create(
        username="jefe_soporte", password=make_password("jefe123"), gerencia=jefatura_soporte
    )
    cliente = CustomUser.objects.create(
        username="cliente", password=make_password("cliente123"), gerencia=jefatura_soporte
    )
    agente = CustomUser.objects.create(
        username="agente", password=make_password("agente123"), gerencia=jefatura_soporte
    )

    # 3. Crear catálogos
    # Tipos de dispositivos
    tipo_computo = TipoDispositivo.objects.create(nombre="De cómputo", is_active=True)
    tipo_red = TipoDispositivo.objects.create(nombre="De Red", is_active=True)
    tipo_periferico = TipoDispositivo.objects.create(nombre="Periférico", is_active=True)

    # Subtipos de dispositivos
    subtipo_laptop = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_computo, nombre="Laptop", is_active=True)
    subtipo_router = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_red, nombre="Router", is_active=True)
    subtipo_monitor = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_periferico, nombre="Monitor", is_active=True)

    # Características
    caracteristica_ram = Caracteristica.objects.create(nombre="RAM", is_active=True)
    caracteristica_disco = Caracteristica.objects.create(nombre="Disco Duro", is_active=True)

    # Características asociadas a subtipos
    CaracteristicaTipoDispositivo.objects.create(caracteristica=caracteristica_ram, subtipo_dispositivo=subtipo_laptop, obligatorio=True)
    CaracteristicaTipoDispositivo.objects.create(caracteristica=caracteristica_disco, subtipo_dispositivo=subtipo_laptop, obligatorio=True)

    # Estados de dispositivo
    estado_activo = EstadoDispositivo.objects.create(nombre="Activo", descripcion="En uso", is_active=True)
    estado_reparacion = EstadoDispositivo.objects.create(nombre="En reparación", descripcion="En taller", is_active=True)

    # Ubicaciones
    ubicacion_norte = Ubicacion.objects.create(agencia="Agencia Central", piso="Piso 1", zona="Norte", is_active=True)
    ubicacion_centro = Ubicacion.objects.create(agencia="Agencia Central", piso="Piso 2", zona="Centro", is_active=True)

    # Marcas y modelos
    marca_dell = Marca.objects.create(nombre="Dell", is_active=True)
    modelo_xps = Modelo.objects.create(nombre="XPS 13", marca_id_marca=marca_dell, is_active=True)

    # Cantidad y tipo de memoria
    memoria_16gb = CantidadMemoria.objects.create(cantidad=16, is_active=True)
    tipo_ddr4 = TipoMemoria.objects.create(nombre="DDR4", is_active=True)

    # Procesadores
    procesador_i7 = Procesador.objects.create(marca=marca_dell, modelo="Core i7-12700", velocidad="2.1 GHz", nucleos=12, is_active=True)

    # 4. Crear dispositivos
    dispositivo_laptop = Dispositivo.objects.create(
        nomenclatura="LAP-001", serie="SN12345", jira="JIRA-001",
        tipo_dispositivo=tipo_computo, subtipo_dispositivo=subtipo_laptop,
        propietario=cliente, is_active=True
    )
    dispositivo_router = Dispositivo.objects.create(
        nomenclatura="RTR-001", serie="SN67890", jira="JIRA-002",
        tipo_dispositivo=tipo_red, subtipo_dispositivo=subtipo_router,
        propietario=cliente, is_active=True
    )

    # 5. Asignar características a dispositivos
    DispositivoCaracteristica.objects.create(
        dispositivo=dispositivo_laptop, caracteristica=caracteristica_ram, valor="16GB"
    )
    DispositivoCaracteristica.objects.create(
        dispositivo=dispositivo_laptop, procesador=procesador_i7
    )

    # 6. Registrar historiales
    # Estado
    DispositivoEstado.objects.create(
        fecha=datetime.date(2025, 3, 1), comentario="Dispositivo activado",
        dispositivo_id_dispositivo=dispositivo_laptop, estado_id_estado=estado_activo,
        agente=agente, is_active=True
    )
    # Ubicación
    DispositivoUbicacion.objects.create(
        fecha=datetime.date(2025, 3, 1), comentario="Asignado a Piso 1",
        dispositivo_id_dispositivo=dispositivo_laptop, ubicacion_id_ubicacion=ubicacion_norte,
        agente=agente, is_active=True
    )
    # Cambio de propietario
    DispositivoPropietarioHistorico.objects.create(
        dispositivo=dispositivo_laptop, propietario=cliente,
        fecha_cambio=datetime.datetime(2025, 3, 1, 10, 0), comentario="Asignación inicial",
        agente=agente, is_active=True
    )

    print("Base de datos poblada con éxito!")

if __name__ == "__main__":
    populate_db()