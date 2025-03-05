import os
import django
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIT.settings')
try:
    django.setup()
    print("Django configurado correctamente.")
except Exception as e:
    print(f"Error configurando Django: {e}")
    exit(1)

from django.contrib.auth.models import Group
from custom_auth.models import CustomUser
from inventario.models import (
    Gerencia, TipoDispositivo, SubtipoDispositivo, EstadoDispositivo, Ubicacion, Marca, Modelo,
    Caracteristica, CantidadMemoria, TipoMemoria, Procesador, CaracteristicaTipoDispositivo, Dispositivo,
    DispositivoCaracteristica, DispositivoEstado, DispositivoUbicacion,
    DispositivoPropietarioHistorico
)

def populate_db():
    print("Iniciando poblamiento de la base de datos...")
    try:
        # Crear grupos
        for group_name in ['Cliente', 'Jefe', 'Subgerente', 'Gerente', 'Gerente General', 'Agente', 'Administrador']:
            Group.objects.get_or_create(name=group_name)
        print("Grupos creados exitosamente.")

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
        print("Gerencias creadas exitosamente.")

        # Crear usuarios
        gerente_general = CustomUser.objects.create_user(username='gerente_general', password='pass123', gerencia=gerencia_general)
        gerente_general.groups.add(Group.objects.get(name='Gerente General'))
        print("Usuario gerente_general creado exitosamente.")

        gerente_operativa = CustomUser.objects.create_user(username='gerente_operativa', password='pass123', gerencia=gerencia_operativa)
        gerente_operativa.groups.add(Group.objects.get(name='Gerente'))
        print("Usuario gerente_operativa creado exitosamente.")

        gerente_rrhh = CustomUser.objects.create_user(username='gerente_rrhh', password='pass123', gerencia=gerencia_rrhh)
        gerente_rrhh.groups.add(Group.objects.get(name='Gerente'))
        print("Usuario gerente_rrhh creado exitosamente.")

        subgerente_it = CustomUser.objects.create_user(username='subgerente_it', password='pass123', gerencia=subgerencia_it)
        subgerente_it.groups.add(Group.objects.get(name='Subgerente'))
        print("Usuario subgerente_it creado exitosamente.")

        subgerente_recursos = CustomUser.objects.create_user(username='subgerente_recursos', password='pass123', gerencia=subgerencia_recursos)
        subgerente_recursos.groups.add(Group.objects.get(name='Subgerente'))
        print("Usuario subgerente_recursos creado exitosamente.")

        jefe_redes = CustomUser.objects.create_user(username='jefe_redes', password='pass123', gerencia=jefatura_redes)
        jefe_redes.groups.add(Group.objects.get(name='Jefe'))
        print("Usuario jefe_redes creado exitosamente.")

        jefe_soporte = CustomUser.objects.create_user(username='jefe_soporte', password='pass123', gerencia=jefatura_soporte)
        jefe_soporte.groups.add(Group.objects.get(name='Jefe'))
        print("Usuario jefe_soporte creado exitosamente.")

        jefe_personal = CustomUser.objects.create_user(username='jefe_personal', password='pass123', gerencia=jefatura_personal)
        jefe_personal.groups.add(Group.objects.get(name='Jefe'))
        print("Usuario jefe_personal creado exitosamente.")

        jefe_capacitacion = CustomUser.objects.create_user(username='jefe_capacitacion', password='pass123', gerencia=jefatura_capacitacion)
        jefe_capacitacion.groups.add(Group.objects.get(name='Jefe'))
        print("Usuario jefe_capacitacion creado exitosamente.")

        cliente_redes1 = CustomUser.objects.create_user(username='cliente_redes1', password='pass123', gerencia=jefatura_redes)
        cliente_redes1.groups.add(Group.objects.get(name='Cliente'))
        print("Usuario cliente_redes1 creado exitosamente.")

        cliente_redes2 = CustomUser.objects.create_user(username='cliente_redes2', password='pass123', gerencia=jefatura_redes)
        cliente_redes2.groups.add(Group.objects.get(name='Cliente'))
        print("Usuario cliente_redes2 creado exitosamente.")

        cliente_soporte = CustomUser.objects.create_user(username='cliente_soporte', password='pass123', gerencia=jefatura_soporte)
        cliente_soporte.groups.add(Group.objects.get(name='Cliente'))
        print("Usuario cliente_soporte creado exitosamente.")

        cliente_personal = CustomUser.objects.create_user(username='cliente_personal', password='pass123', gerencia=jefatura_personal)
        cliente_personal.groups.add(Group.objects.get(name='Cliente'))
        print("Usuario cliente_personal creado exitosamente.")

        cliente_capacitacion = CustomUser.objects.create_user(username='cliente_capacitacion', password='pass123', gerencia=jefatura_capacitacion)
        cliente_capacitacion.groups.add(Group.objects.get(name='Cliente'))
        print("Usuario cliente_capacitacion creado exitosamente.")

        agente = CustomUser.objects.create_user(username='agente1', password='pass123', gerencia=subgerencia_it)
        agente.groups.add(Group.objects.get(name='Agente'))
        print("Usuario agente1 creado exitosamente.")

        admin = CustomUser.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        admin.groups.add(Group.objects.get(name='Administrador'))
        print("Usuario admin creado exitosamente.")

        # Crear catálogos de memoria
        cantidad_8gb = CantidadMemoria.objects.create(cantidad=8)
        cantidad_16gb = CantidadMemoria.objects.create(cantidad=16)
        tipo_ddr4 = TipoMemoria.objects.create(nombre="DDR4")
        tipo_ddr5 = TipoMemoria.objects.create(nombre="DDR5")
        print("Catálogos de memoria creados exitosamente.")

        # Crear catálogos
        tipo_computo = TipoDispositivo.objects.create(nombre="De cómputo")
        tipo_red = TipoDispositivo.objects.create(nombre="De red")
        tipo_periferico = TipoDispositivo.objects.create(nombre="Periférico")
        print("Tipos de dispositivos creados exitosamente.")

        # Crear subtipos
        subtipo_notebook = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_computo, nombre="Notebook")
        subtipo_pc = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_computo, nombre="PC de escritorio")
        subtipo_switch = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_red, nombre="Switch")
        subtipo_impresora = SubtipoDispositivo.objects.create(tipo_dispositivo=tipo_periferico, nombre="Impresora")
        print("Subtipos de dispositivos creados exitosamente.")

        estado_activo = EstadoDispositivo.objects.create(nombre="Activo")
        estado_reparacion = EstadoDispositivo.objects.create(nombre="En reparación")
        estado_baja = EstadoDispositivo.objects.create(nombre="Dado de baja")
        print("Estados de dispositivos creados exitosamente.")

        ubicacion_central = Ubicacion.objects.create(agencia="Agencia Central", piso="1", zona="Norte")
        ubicacion_sur = Ubicacion.objects.create(agencia="Agencia Sur", piso="2", zona="Centro")
        ubicacion_norte = Ubicacion.objects.create(agencia="Agencia Norte", piso="3", zona="Norte")
        print("Ubicaciones creadas exitosamente.")

        marca_dell = Marca.objects.create(nombre="Dell")
        marca_cisco = Marca.objects.create(nombre="Cisco")
        marca_hp = Marca.objects.create(nombre="HP")
        print("Marcas creadas exitosamente.")

        modelo_dell_notebook = Modelo.objects.create(nombre="Latitude 5400", marca_id_marca=marca_dell)
        modelo_dell_pc = Modelo.objects.create(nombre="OptiPlex 5000", marca_id_marca=marca_dell)
        modelo_cisco_switch = Modelo.objects.create(nombre="Catalyst 9200", marca_id_marca=marca_cisco)
        modelo_hp_impresora = Modelo.objects.create(nombre="LaserJet 200", marca_id_marca=marca_hp)
        print("Modelos creados exitosamente.")

        carac_procesador = Caracteristica.objects.create(nombre="Procesador")
        carac_ram = Caracteristica.objects.create(nombre="RAM")
        carac_velocidad = Caracteristica.objects.create(nombre="Velocidad de red")
        carac_tipo = Caracteristica.objects.create(nombre="Tipo periférico")
        print("Características creadas exitosamente.")

        # Asociar características a subtipos
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_procesador, subtipo_dispositivo=subtipo_notebook, obligatorio=True)
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_procesador, subtipo_dispositivo=subtipo_pc, obligatorio=True)
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_ram, subtipo_dispositivo=subtipo_notebook, obligatorio=True)
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_ram, subtipo_dispositivo=subtipo_pc, obligatorio=True)
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_velocidad, subtipo_dispositivo=subtipo_switch, obligatorio=True)
        CaracteristicaTipoDispositivo.objects.create(caracteristica=carac_tipo, subtipo_dispositivo=subtipo_impresora, obligatorio=True)
        print("Características asociadas a subtipos exitosamente.")

        # Crear procesadores
        procesador_i5 = Procesador.objects.create(marca=marca_dell, modelo="Intel i5-1135G7", velocidad="2.4 GHz", nucleos=4)
        procesador_i7 = Procesador.objects.create(marca=marca_dell, modelo="Intel i7-1185G7", velocidad="3.0 GHz", nucleos=4)
        print("Procesadores creados exitosamente.")

        # Crear dispositivos de los tres tipos
        # Dispositivos tipo "De cómputo"
        notebook_redes1 = Dispositivo.objects.create(nomenclatura="NOTEBOOK-REDES-001", tipo_dispositivo=tipo_computo, subtipo_dispositivo=subtipo_notebook, propietario=cliente_redes1, is_active=True)
        pc_redes2 = Dispositivo.objects.create(nomenclatura="PC-REDES-002", tipo_dispositivo=tipo_computo, subtipo_dispositivo=subtipo_pc, propietario=cliente_redes2, is_active=True)
        pc_soporte = Dispositivo.objects.create(nomenclatura="PC-SOPORTE-001", tipo_dispositivo=tipo_computo, subtipo_dispositivo=subtipo_pc, propietario=cliente_soporte, is_active=True)
        print("Dispositivos tipo 'De cómputo' creados exitosamente.")

        # Dispositivos tipo "De red"
        switch_redes = Dispositivo.objects.create(nomenclatura="SW-REDES-001", tipo_dispositivo=tipo_red, subtipo_dispositivo=subtipo_switch, propietario=jefe_redes, is_active=True)
        print("Dispositivos tipo 'De red' creados exitosamente.")

        # Dispositivos tipo "Periférico"
        impresora_capacitacion = Dispositivo.objects.create(nomenclatura="PRINT-CAP-001", tipo_dispositivo=tipo_periferico, subtipo_dispositivo=subtipo_impresora, propietario=jefe_capacitacion, is_active=True)
        print("Dispositivos tipo 'Periférico' creados exitosamente.")

        # Características para dispositivos tipo "De cómputo" (incluyendo memoria y procesador)
        DispositivoCaracteristica.objects.create(dispositivo=notebook_redes1, procesador=procesador_i5)
        DispositivoCaracteristica.objects.create(dispositivo=notebook_redes1, caracteristica=carac_ram, valor=f"{cantidad_16gb.cantidad} {tipo_ddr5.nombre}")
        DispositivoCaracteristica.objects.create(dispositivo=pc_redes2, procesador=procesador_i7)
        DispositivoCaracteristica.objects.create(dispositivo=pc_redes2, caracteristica=carac_ram, valor=f"{cantidad_8gb.cantidad} {tipo_ddr4.nombre}")
        DispositivoCaracteristica.objects.create(dispositivo=pc_soporte, procesador=procesador_i5)
        DispositivoCaracteristica.objects.create(dispositivo=pc_soporte, caracteristica=carac_ram, valor=f"{cantidad_8gb.cantidad} {tipo_ddr4.nombre}")
        print("Características para dispositivos tipo 'De cómputo' creadas exitosamente.")

        # Características para dispositivos tipo "De red"
        DispositivoCaracteristica.objects.create(dispositivo=switch_redes, caracteristica=carac_velocidad, valor="1Gbps")
        print("Características para dispositivos tipo 'De red' creadas exitosamente.")

        # Características para dispositivos tipo "Periférico"
        DispositivoCaracteristica.objects.create(dispositivo=impresora_capacitacion, caracteristica=carac_tipo, valor="Impresora")
        print("Características para dispositivos tipo 'Periférico' creadas exitosamente.")

        # Historiales
        DispositivoEstado.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=notebook_redes1, estado_id_estado=estado_activo, agente=agente)
        DispositivoEstado.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=pc_redes2, estado_id_estado=estado_reparacion, agente=agente)
        DispositivoEstado.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=switch_redes, estado_id_estado=estado_activo, agente=agente)
        DispositivoEstado.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=pc_soporte, estado_id_estado=estado_activo, agente=agente)
        DispositivoEstado.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=impresora_capacitacion, estado_id_estado=estado_activo, agente=agente)
        print("Historiales de estado creados exitosamente.")

        DispositivoUbicacion.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=notebook_redes1, ubicacion_id_ubicacion=ubicacion_central, agente=agente)
        DispositivoUbicacion.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=pc_redes2, ubicacion_id_ubicacion=ubicacion_norte, agente=agente)
        DispositivoUbicacion.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=switch_redes, ubicacion_id_ubicacion=ubicacion_central, agente=agente)
        DispositivoUbicacion.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=pc_soporte, ubicacion_id_ubicacion=ubicacion_sur, agente=agente)
        DispositivoUbicacion.objects.create(fecha="2025-03-01", dispositivo_id_dispositivo=impresora_capacitacion, ubicacion_id_ubicacion=ubicacion_norte, agente=agente)
        print("Historiales de ubicación creados exitosamente.")

        DispositivoPropietarioHistorico.objects.create(
            dispositivo=notebook_redes1, propietario_id_nuevo=cliente_redes1, fecha_cambio=timezone.now(), agente=agente
        )
        DispositivoPropietarioHistorico.objects.create(
            dispositivo=switch_redes, propietario_id_nuevo=jefe_redes, fecha_cambio=timezone.now(), agente=agente
        )
        print("Historiales de propietario creados exitosamente.")

        print("Base de datos poblada con éxito.")
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")

if __name__ == "__main__":
    print("Ejecutando populate_db.py...")
    populate_db()