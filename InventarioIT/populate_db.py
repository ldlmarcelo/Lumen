import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIT.settings')
django.setup()

from django.contrib.auth.models import Group
from custom_auth.models import CustomUser
from inventario.models import (
    Gerencia, TipoDispositivo, EstadoDispositivo, Ubicacion, Marca, Modelo,
    Caracteristica, CaracteristicaTipoDispositivo, Dispositivo,
    DispositivoCaracteristica, DispositivoEstado, DispositivoUbicacion,
    DispositivoPropietarioHistorico
)

def populate_db():
    # Crear grupos
    for group_name in ['Cliente', 'Jefe', 'Subgerente', 'Gerente', 'Gerente General', 'Agente', 'Administrador']:
        Group.objects.get_or_create(name=group_name)

    # Crear gerencias (jerarquía)
    gerencia_general = Gerencia.objects.create(nombre="Gerencia General")
    gerencia_operativa = Gerencia.objects.create(nombre="Gerencia Operativa", parent=gerencia_general)
    subgerencia_it = Gerencia.objects.create(nombre="Subgerencia IT", parent=gerencia_operativa)
    jefatura_redes = Gerencia.objects.create(nombre="Jefatura Redes", parent=subgerencia_it)
    jefatura_soporte = Gerencia.objects.create(nombre="Jefatura Soporte", parent=subgerencia_it)
    gerencia_rrhh = Gerencia.objects.create(nombre="Gerencia RRHH", parent=gerencia_general)
    subgerencia_recursos = Gerencia.objects.create(nombre="Subgerencia Recursos", parent=gerencia_rrhh)
    jefatura_personal = Gerencia.objects.create(nombre="Jefatura Personal", parent=subgerencia_recursos)
    jefatura_capacitacion = Gerencia.objects.create(nombre="Jefatura Capacitación", parent=gerencia_rrhh)

    # Crear usuarios
    gerente_general = CustomUser.objects.create_user(username='gerente_general', password='pass123', gerencia=gerencia_general)
    gerente_general.groups.add(Group.objects.get(name='Gerente General'))

    gerente_operativa = CustomUser.objects.create_user(username='gerente_operativa', password='pass123', gerencia=gerencia_operativa)
    gerente_operativa.groups.add(Group.objects.get(name='Gerente'))

    gerente_rrhh = CustomUser.objects.create_user(username='gerente_rrhh', password='pass123', gerencia=gerencia_rrhh)
    gerente_rrhh.groups.add(Group.objects.get(name='Gerente'))

    subgerente_it = CustomUser.objects.create_user(username='subgerente_it', password='pass123', gerencia=subgerencia_it)
    subgerente_it.groups.add(Group.objects.get(name='Subgerente'))

    subgerente_recursos = CustomUser.objects.create_user(username='subgerente_recursos', password='pass123', gerencia=subgerencia_recursos)
    subgerente_recursos.groups.add(Group.objects.get(name='Subgerente'))

    jefe_redes = CustomUser.objects.create_user(username='jefe_redes', password='pass123', gerencia=jefatura_redes)
    jefe_redes.groups.add(Group.objects.get(name='Jefe'))

    jefe_soporte = CustomUser.objects.create_user(username='jefe_soporte', password='pass123', gerencia=jefatura_soporte)
    jefe_soporte.groups.add(Group.objects.get(name='Jefe'))

    jefe_personal = CustomUser.objects.create_user(username='jefe_personal', password='pass123', gerencia=jefatura_personal)
    jefe_personal.groups.add(Group.objects.get(name='Jefe'))

    jefe_capacitacion = CustomUser.objects.create_user(username='jefe_capacitacion', password='pass123', gerencia=jefatura_capacitacion)
    jefe_capacitacion.groups.add(Group.objects.get(name='Jefe'))

    cliente_redes1 = CustomUser.objects.create_user(username='cliente_redes1', password='pass123', gerencia=jefatura_redes)
    cliente_redes1.groups.add(Group.objects.get(name='Cliente'))

    cliente_redes2 = CustomUser.objects.create_user(username='cliente_redes2', password='pass123', gerencia=jefatura_redes)
    cliente_redes2.groups.add(Group.objects.get(name='Cliente'))

    cliente_soporte = CustomUser.objects.create_user(username='cliente_soporte', password='pass123', gerencia=jefatura_soporte)
    cliente_soporte.groups.add(Group.objects.get(name='Cliente'))

    cliente_personal = CustomUser.objects.create_user(username='cliente_personal', password='pass123', gerencia=jefatura_personal)
    cliente_personal.groups.add(Group.objects.get(name='Cliente'))

    cliente_capacitacion = CustomUser.objects.create_user(username='cliente_capacitacion', password='pass123', gerencia=jefatura_capacitacion)
    cliente_capacitacion.groups.add(Group.objects.get(name='Cliente'))

    agente = CustomUser.objects.create_user(username='agente1', password='pass123', gerencia=subgerencia_it)
    agente.groups.add(Group.objects.get(name='Agente'))

    admin = CustomUser.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
    admin.groups.add(Group.objects.get(name='Administrador'))

    # Crear catálogos
    tipo_computo = TipoDispositivo.objects.create(nombre="De cómputo")
    tipo_red = TipoDispositivo.objects.create(nombre="De red")
    tipo_periferico = TipoDispositivo.objects.create(nombre="Periférico")

    estado_activo = EstadoDispositivo.objects.create(nombre="Activo")
    estado_reparacion = EstadoDispositivo.objects.create(nombre="En reparación")
    estado_baja = EstadoDispositivo.objects.create(nombre="Dado de baja")

    ubicacion_central = Ubicacion.objects.create(agencia="Agencia Central", piso="1", zona="Norte")
    ubicacion_sur = Ubicacion.objects.create(agencia="Agencia Sur", piso="2", zona="Centro")
    ubicacion_norte = Ubicacion.objects.create(agencia="Agencia Norte", piso="3", zona="Norte")

    marca_dell = Marca.objects.create(nombre="Dell")
    marca_cisco = Marca.objects.create(nombre="Cisco")
    marca_hp = Marca.objects.create(nombre="HP")

    modelo_dell_pc = Modelo.objects.create(nombre="Latitude 5400", marca_id_marca=marca_dell)
    modelo_cisco_sw = Modelo.objects.create(nombre="Catalyst 9200", marca_id_marca=marca_cisco)
    modelo_hp_print = Modelo.objects.create(nombre="LaserJet 200", marca_id_marca=marca_hp)

    carac_procesador = Caracteristica.objects.create(nombre="Procesador")
    carac_ram = Caracteristica.objects.create(nombre="RAM")
    carac_velocidad = Caracteristica.objects.create(nombre="Velocidad de red")
    carac_tipo = Caracteristica.objects.create(nombre="Tipo periférico")

    CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_procesador, tipo_dispositivo=tipo_computo, obligatorio=True)
    CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_ram, tipo_dispositivo=tipo_computo)
    CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_velocidad, tipo_dispositivo=tipo_red, obligatorio=True)
    CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_tipo, tipo_dispositivo=tipo_periferico)

    # Crear dispositivos
    pc_redes1 = Dispositivo.objects.create(nomenclatura="PC-REDES-001", tipo_dispositivo=tipo_computo, propietario=cliente_redes1, is_active=True)
    pc_redes2 = Dispositivo.objects.create(nomenclatura="PC-REDES-002", tipo_dispositivo=tipo_computo, propietario=cliente_redes2, is_active=True)
    sw_redes = Dispositivo.objects.create(nomenclatura="SW-REDES-001", tipo_dispositivo=tipo_red, propietario=jefe_redes, is_active=True)
    pc_soporte = Dispositivo.objects.create(nomenclatura="PC-SOPORTE-001", tipo_dispositivo=tipo_computo, propietario=cliente_soporte, is_active=True)
    pc_personal = Dispositivo.objects.create(nomenclatura="PC-PERS-001", tipo_dispositivo=tipo_computo, propietario=cliente_personal, is_active=True)
    pc_capacitacion = Dispositivo.objects.create(nomenclatura="PC-CAP-001", tipo_dispositivo=tipo_computo, propietario=cliente_capacitacion, is_active=True)
    print_capacitacion = Dispositivo.objects.create(nomenclatura="PRINT-CAP-001", tipo_dispositivo=tipo_periferico, propietario=jefe_capacitacion, is_active=True)

    # Características
    DispositivoCaracter