from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

# Catálogos
class Gerencia(MPTTModel):
    id_gerencia = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name="Gerencia Superior")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class MPTTMeta:
        order_insertion_by = ['nombre']

    def clean(self):
        if not self.is_active and Gerencia.objects.filter(nombre=self.nombre, is_active=False).exclude(id_gerencia=self.id_gerencia).exists():
            raise ValidationError("Ya existe una gerencia inactiva con este nombre.")

    def __str__(self):
        return self.nombre

class TipoDispositivo(models.Model):
    id_tipo_dispositivo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and TipoDispositivo.objects.filter(nombre=self.nombre, is_active=False).exclude(id_tipo_dispositivo=self.id_tipo_dispositivo).exists():
            raise ValidationError("Ya existe un tipo de dispositivo inactivo con este nombre.")

    def __str__(self):
        return self.nombre

class SubtipoDispositivo(models.Model):
    id_subtipo_dispositivo = models.AutoField(primary_key=True)
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, on_delete=models.CASCADE, verbose_name="Tipo de Dispositivo")
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('tipo_dispositivo', 'nombre')

    def clean(self):
        if not self.is_active and SubtipoDispositivo.objects.filter(
            tipo_dispositivo=self.tipo_dispositivo, nombre=self.nombre, is_active=False
        ).exclude(id_subtipo_dispositivo=self.id_subtipo_dispositivo).exists():
            raise ValidationError("Ya existe un subtipo inactivo con este nombre para este tipo.")

    def __str__(self):
        return f"{self.tipo_dispositivo.nombre} - {self.nombre}"

class Caracteristica(models.Model):
    id_caracteristica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and Caracteristica.objects.filter(nombre=self.nombre, is_active=False).exclude(id_caracteristica=self.id_caracteristica).exists():
            raise ValidationError("Ya existe una característica inactiva con este nombre.")

    def __str__(self):
        return self.nombre

class CaracteristicaTipoDispositivo(models.Model):
    id_caracteristica_tipo = models.AutoField(primary_key=True)
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE, verbose_name="Característica")
    subtipo_dispositivo = models.ForeignKey(SubtipoDispositivo, on_delete=models.CASCADE, verbose_name="Subtipo de Dispositivo")
    obligatorio = models.BooleanField(default=False, verbose_name="Obligatorio")

    class Meta:
        unique_together = ('caracteristica', 'subtipo_dispositivo')

    def __str__(self):
        return f"{self.caracteristica.nombre} ({self.subtipo_dispositivo})"
    
class EstadoDispositivo(models.Model):
    id_estado_dispositivo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and EstadoDispositivo.objects.filter(nombre=self.nombre, is_active=False).exclude(id_estado_dispositivo=self.id_estado_dispositivo).exists():
            raise ValidationError("Ya existe un estado de dispositivo inactivo con este nombre.")

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    ZONA_CHOICES = [('Norte', 'Zona Norte'), ('Centro', 'Zona Centro')]
    id_ubicacion = models.AutoField(primary_key=True)
    agencia = models.CharField(max_length=45, unique=False, verbose_name="Agencia")
    piso = models.CharField(max_length=45, blank=True, null=True, verbose_name="Piso")
    zona = models.CharField(max_length=10, choices=ZONA_CHOICES, default='Norte', verbose_name="Zona")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('agencia', 'piso', 'zona')

    def clean(self):
        if not self.is_active and Ubicacion.objects.filter(agencia=self.agencia, piso=self.piso, zona=self.zona, is_active=False).exclude(id_ubicacion=self.id_ubicacion).exists():
            raise ValidationError("Ya existe una ubicación inactiva con estos valores.")

    def __str__(self):
        return f"{self.agencia} - Piso {self.piso} - {self.zona}"

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and Marca.objects.filter(nombre=self.nombre, is_active=False).exclude(id_marca=self.id_marca).exists():
            raise ValidationError("Ya existe una marca inactiva con este nombre.")

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    marca_id_marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, db_column='marca_id_marca', verbose_name="Marca")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('nombre', 'marca_id_marca')

    def clean(self):
        if not self.is_active and Modelo.objects.filter(nombre=self.nombre, marca_id_marca=self.marca_id_marca, is_active=False).exclude(id_modelo=self.id_modelo).exists():
            raise ValidationError("Ya existe un modelo inactivo con este nombre y marca.")

    def __str__(self):
        return f"{self.marca_id_marca.nombre} - {self.nombre}"

class CantidadMemoria(models.Model):
    id_cantidad_memoria = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(unique=True, verbose_name="Cantidad (GB)")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and CantidadMemoria.objects.filter(cantidad=self.cantidad, is_active=False).exclude(id_cantidad_memoria=self.id_cantidad_memoria).exists():
            raise ValidationError("Ya existe una cantidad de memoria inactiva con este valor.")

    def __str__(self):
        return str(self.cantidad)

class TipoMemoria(models.Model):
    id_tipo_memoria = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=45, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def clean(self):
        if not self.is_active and TipoMemoria.objects.filter(nombre=self.nombre, is_active=False).exclude(id_tipo_memoria=self.id_tipo_memoria).exists():
            raise ValidationError("Ya existe un tipo de memoria inactivo con este nombre.")

    def __str__(self):
        return self.nombre

class Procesador(models.Model):
    id_procesador = models.AutoField(primary_key=True)
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, verbose_name="Marca")
    modelo = models.CharField(max_length=100, unique=True, verbose_name="Modelo")
    velocidad = models.CharField(max_length=20, verbose_name="Velocidad (GHz)")  # Ej. "2.4 GHz"
    nucleos = models.PositiveIntegerField(verbose_name="Núcleos")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        unique_together = ('marca', 'modelo')

    def clean(self):
        if not self.is_active and Procesador.objects.filter(marca=self.marca, modelo=self.modelo, is_active=False).exclude(id_procesador=self.id_procesador).exists():
            raise ValidationError("Ya existe un procesador inactivo con esta marca y modelo.")

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo} ({self.velocidad}, {self.nucleos} núcleos)"

# Dispositivos
class Dispositivo(models.Model):
    id_dispositivo = models.AutoField(primary_key=True)
    nomenclatura = models.CharField(unique=True, max_length=45, verbose_name="Nomenclatura")
    serie = models.CharField(max_length=45, blank=True, null=True, verbose_name="Número de Serie")
    jira = models.CharField(max_length=45, blank=True, null=True, verbose_name="Jira Ticket")
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, on_delete=models.DO_NOTHING, verbose_name="Tipo de Dispositivo")
    subtipo_dispositivo = models.ForeignKey(SubtipoDispositivo, on_delete=models.DO_NOTHING, verbose_name="Subtipo de Dispositivo")
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Propietario")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nomenclatura
    
class DispositivoCaracteristica(models.Model):
    id_dispositivo_caracteristica = models.AutoField(primary_key=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, verbose_name="Dispositivo")
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE, verbose_name="Característica", null=True, blank=True)
    procesador = models.ForeignKey(Procesador, on_delete=models.CASCADE, verbose_name="Procesador", null=True, blank=True)
    valor = models.CharField(max_length=45, null=True, blank=True, verbose_name="Valor")  # Mantener para características no procesadores

    class Meta:
        unique_together = ('dispositivo', 'caracteristica', 'procesador')

    def clean(self):
        if not self.dispositivo or not self.dispositivo.tipo_dispositivo:
            raise ValidationError("El dispositivo debe estar definido y tener un tipo.")
        
        if self.dispositivo.tipo_dispositivo.nombre == "De cómputo":
            if not self.procesador:
                raise ValidationError({
                    'procesador': "No se ha asignado un procesador al equipo. Se guardará sin procesador, pero considera asignar uno para completar la información."
                })
        elif self.procesador:
            raise ValidationError("Los dispositivos que no son tipo 'De cómputo' no pueden tener un procesador asignado.")

        if self.caracteristica and self.procesador:
            raise ValidationError("No se puede asignar tanto una característica como un procesador a la misma relación.")

    def __str__(self):
        if self.procesador:
            return f"{self.dispositivo.nomenclatura} - Procesador: {self.procesador}"
        if self.caracteristica:
            return f"{self.dispositivo.nomenclatura} - {self.caracteristica.nombre}: {self.valor}"
        return f"{self.dispositivo.nomenclatura} - Característica no especificada"

# Historiales
class DispositivoEstado(models.Model):
    id_dispositivo_estado = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name="Fecha")
    comentario = models.CharField(max_length=45, blank=True, null=True, verbose_name="Comentario")
    dispositivo_id_dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, db_column='dispositivo_id_dispositivo', verbose_name="Dispositivo")
    estado_id_estado = models.ForeignKey('EstadoDispositivo', on_delete=models.DO_NOTHING, db_column='estado_id_estado', verbose_name="Estado")
    agente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Agente del Cambio de Estado", related_name='cambios_estado_dispositivo')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Dispositivo Estado"
        verbose_name_plural = "Dispositivos Estados"

    def __str__(self):
        return f"{self.dispositivo_id_dispositivo.nomenclatura} - {self.fecha} - {self.estado_id_estado.nombre}"

class DispositivoUbicacion(models.Model):
    id_dispositivo_ubicacion = models.AutoField(primary_key=True)
    fecha = models.DateField(verbose_name="Fecha")
    comentario = models.CharField(max_length=45, blank=True, null=True, verbose_name="Comentario")
    dispositivo_id_dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, db_column='dispositivo_id_dispositivo', verbose_name="Dispositivo")
    ubicacion_id_ubicacion = models.ForeignKey('Ubicacion', on_delete=models.DO_NOTHING, db_column='ubicacion_id_ubicacion', verbose_name="Ubicación")
    agente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Agente del Cambio de Ubicación", related_name='cambios_ubicacion_dispositivo')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Dispositivo Ubicación"
        verbose_name_plural = "Dispositivos Ubicaciones"

    def __str__(self):
        return f"{self.dispositivo_id_dispositivo.nomenclatura} - {self.fecha} - {self.ubicacion_id_ubicacion.agencia}, {self.ubicacion_id_ubicacion.piso}"


class DispositivoPropietarioHistorico(models.Model):
    id_dispositivo_propietario_historico = models.AutoField(primary_key=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, verbose_name="Dispositivo")
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Propietario")
    fecha_cambio = models.DateTimeField(verbose_name="Fecha de Cambio")
    comentario = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comentario")
    agente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Agente del Cambio de Propietario", related_name='cambios_propietario_historico')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Dispositivo Propietario Histórico"
        verbose_name_plural = "Dispositivos Propietarios Históricos"
        ordering = ['fecha_cambio']  # Para facilitar el orden cronológico

    def __str__(self):
        return f"{self.dispositivo.nomenclatura} - {self.fecha_cambio} - Propietario: {self.propietario}"

    def save(self, *args, **kwargs):
        # Opcional: Validar que el propietario sea diferente al del último registro
        if self.pk is None:  # Solo en creación de nuevo registro
            ultimo_registro = DispositivoPropietarioHistorico.objects.filter(
                dispositivo=self.dispositivo
            ).order_by('-fecha_cambio').first()
            if ultimo_registro and ultimo_registro.propietario == self.propietario:
                raise ValidationError("El propietario no ha cambiado.")
        super().save(*args, **kwargs)