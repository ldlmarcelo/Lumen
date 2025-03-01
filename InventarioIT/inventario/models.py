from django.db import models
from django.conf import settings

# Catálogos
class Gerencia(models.Model):
    id_gerencia = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class TipoDispositivo(models.Model):
    id_tipo_dispositivo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class EstadoDispositivo(models.Model):
    id_estado_dispositivo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    agencia = models.CharField(max_length=45, unique=False, verbose_name="Agencia")
    piso = models.CharField(max_length=45, blank=True, null=True, verbose_name="Piso")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('agencia', 'piso')

    def __str__(self):
        return f"{self.agencia} - Piso {self.piso}"

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    marca_id_marca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='marca_id_marca', verbose_name="Marca")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('nombre', 'marca_id_marca')

    def __str__(self):
        return f"{self.marca_id_marca.nombre} - {self.nombre}"

class Caracteristica(models.Model):
    id_caracteristica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class CantidadMemoria(models.Model):
    id_cantidad_memoria = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(unique=True, verbose_name="Cantidad (GB)")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return str(self.cantidad)

class TipoMemoria(models.Model):
    id_tipo_memoria = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class CaracteristicaEspecifica(models.Model):
    id_caracteristica_especifica = models.AutoField(primary_key=True)
    caracteristica = models.ForeignKey(Caracteristica, models.DO_NOTHING, verbose_name="Característica")
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, models.DO_NOTHING, verbose_name="Tipo de Dispositivo")
    tipo_memoria = models.ForeignKey(TipoMemoria, models.DO_NOTHING, blank=True, null=True, verbose_name="Tipo de Memoria")
    cantidad_memoria = models.ForeignKey(CantidadMemoria, models.DO_NOTHING, blank=True, null=True, verbose_name="Cantidad de Memoria")
    tipo_procesador = models.CharField(max_length=45, blank=True, null=True, verbose_name="Tipo de Procesador")
    velocidad_red = models.CharField(max_length=45, blank=True, null=True, verbose_name="Velocidad de Red")
    interfaz_conexion = models.CharField(max_length=45, blank=True, null=True, verbose_name="Interfaz de Conexión")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.caracteristica.nombre} ({self.tipo_dispositivo.nombre})"

# Dispositivos
class Dispositivo(models.Model):
    id_dispositivo = models.AutoField(primary_key=True)
    nomenclatura = models.CharField(unique=True, max_length=45, verbose_name="Nomenclatura")
    serie = models.CharField(max_length=45, blank=True, null=True, verbose_name="Número de Serie")
    jira = models.CharField(max_length=45, blank=True, null=True, verbose_name="Jira Ticket")
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, models.DO_NOTHING, verbose_name="Tipo de Dispositivo")
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, verbose_name="Propietario")

    def __str__(self):
        return self.nomenclatura

class DispositivoCaracteristica(models.Model):
    id_dispositivo_caracteristica = models.AutoField(primary_key=True)
    dispositivo_id_dispositivo = models.ForeignKey(Dispositivo, models.DO_NOTHING, db_column='dispositivo_id_dispositivo', verbose_name="Dispositivo")
    caracteristica_especifica = models.ForeignKey(CaracteristicaEspecifica, models.DO_NOTHING, verbose_name="Característica Específica")
    valor = models.CharField(max_length=45, verbose_name="Valor")

    class Meta:
        db_table = 'dispositivo_caracteristica'
        verbose_name = "Dispositivo Característica"
        verbose_name_plural = "Dispositivos Características"

    def __str__(self):
        return f"{self.dispositivo_id_dispositivo.nomenclatura} - {self.valor}"

# Historiales
class DispositivoEstado(models.Model):
    id_dispositivo_estado = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name="Fecha")
    comentario = models.CharField(max_length=45, blank=True, null=True, verbose_name="Comentario")
    dispositivo_id_dispositivo = models.ForeignKey(Dispositivo, models.CASCADE, db_column='dispositivo_id_dispositivo', verbose_name="Dispositivo")
    estado_id_estado = models.ForeignKey('EstadoDispositivo', models.DO_NOTHING, db_column='estado_id_estado', verbose_name="Estado")
    agente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Agente del Cambio de Estado",
        related_name='cambios_estado_dispositivo'
    )

    class Meta:
        verbose_name = "Dispositivo Estado"
        verbose_name_plural = "Dispositivos Estados"

    def __str__(self):
        return f"{self.dispositivo_id_dispositivo.nomenclatura} - {self.fecha} - {self.estado_id_estado.nombre}"

class DispositivoUbicacion(models.Model):
    id_dispositivo_ubicacion = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name="Fecha")
    comentario = models.CharField(max_length=45, blank=True, null=True, verbose_name="Comentario")
    dispositivo_id_dispositivo = models.ForeignKey(Dispositivo, models.CASCADE, db_column='dispositivo_id_dispositivo', verbose_name="Dispositivo")
    ubicacion_id_ubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, db_column='ubicacion_id_ubicacion', verbose_name="Ubicación")
    agente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Agente del Cambio de Ubicación",
        related_name='cambios_ubicacion_dispositivo'
    )

    class Meta:
        verbose_name = "Dispositivo Ubicación"
        verbose_name_plural = "Dispositivos Ubicaciones"

    def __str__(self):
        return f"{self.dispositivo_id_dispositivo.nomenclatura} - {self.fecha} - {self.ubicacion_id_ubicacion.agencia}, {self.ubicacion_id_ubicacion.piso}"

class DispositivoPropietarioHistorico(models.Model):
    id_dispositivo_propietario_historico = models.AutoField(primary_key=True)
    dispositivo = models.ForeignKey(Dispositivo, models.CASCADE, verbose_name="Dispositivo")
    propietario_id_anterior = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        db_column='propietario_id_anterior',
        blank=True,
        null=True,
        related_name='historico_anterior',
        verbose_name="Propietario Anterior"
    )
    propietario_id_nuevo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        db_column='propietario_id_nuevo',
        related_name='historico_nuevo',
        blank=True,
        null=True,
        verbose_name="Propietario Nuevo"
    )
    fecha_cambio = models.DateTimeField(verbose_name="Fecha de Cambio")
    comentario = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comentario")
    agente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Agente del Cambio de Propietario",
        related_name='cambios_propietario_historico'
    )

    class Meta:
        verbose_name = "Dispositivo Propietario Histórico"
        verbose_name_plural = "Dispositivos Propietarios Históricos"

    def __str__(self):
        return f"{self.dispositivo.nomenclatura} - {self.fecha_cambio} - De: {self.propietario_id_anterior} a: {self.propietario_id_nuevo}"