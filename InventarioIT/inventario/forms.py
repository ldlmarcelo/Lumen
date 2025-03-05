from django import forms
from django.contrib.auth.models import User
from .models import Dispositivo, DispositivoCaracteristica, DispositivoEstado, DispositivoUbicacion, DispositivoPropietarioHistorico, Caracteristica, CantidadMemoria, TipoMemoria, Procesador, SubtipoDispositivo

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nomenclatura', 'tipo_dispositivo', 'subtipo_dispositivo', 'propietario', 'is_active']
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'subtipo_dispositivo': forms.Select(attrs={'class': 'form-control'}),
        }

class DispositivoCaracteristicaForm(forms.ModelForm):
    cantidad_memoria = forms.ModelChoiceField(queryset=CantidadMemoria.objects.all(), required=False, label="Cantidad de RAM", empty_label="Seleccione...")
    tipo_memoria = forms.ModelChoiceField(queryset=TipoMemoria.objects.all(), required=False, label="Tipo de RAM", empty_label="Seleccione...")
    procesador = forms.ModelChoiceField(queryset=Procesador.objects.all(), required=False, label="Procesador", empty_label="Seleccione...")

    class Meta:
        model = DispositivoCaracteristica
        fields = ['dispositivo', 'caracteristica', 'procesador', 'valor']
        widgets = {
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'caracteristica': forms.Select(attrs={'class': 'form-control'}),
            'procesador': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # Deshabilitado, se manejará en la vista
            'valor': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Solo lectura, se generará automáticamente
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'caracteristica' in self.data:
            try:
                caracteristica_id = int(self.data.get('caracteristica'))
                caracteristica = Caracteristica.objects.get(id=caracteristica_id)
                if caracteristica.nombre == "RAM":
                    self.fields['procesador'].widget = forms.HiddenInput()  # Ocultar procesador para RAM
                    self.fields['cantidad_memoria'].required = True
                    self.fields['tipo_memoria'].required = True
                elif caracteristica.nombre == "Procesador":
                    self.fields['cantidad_memoria'].widget = forms.HiddenInput()
                    self.fields['tipo_memoria'].widget = forms.HiddenInput()
                    self.fields['procesador'].required = True
                    self.fields['procesador'].widget = forms.Select(attrs={'class': 'form-control'})
                    self.fields['valor'].widget = forms.HiddenInput()  # Ocultar valor para procesador
                else:
                    self.fields['cantidad_memoria'].widget = forms.HiddenInput()
                    self.fields['tipo_memoria'].widget = forms.HiddenInput()
                    self.fields['procesador'].widget = forms.HiddenInput()
            except (ValueError, Caracteristica.DoesNotExist):
                pass
        elif self.instance.pk:
            if self.instance.caracteristica.nombre == "RAM":
                self.fields['procesador'].widget = forms.HiddenInput()
                self.fields['cantidad_memoria'].required = True
                self.fields['tipo_memoria'].required = True
            elif self.instance.caracteristica.nombre == "Procesador":
                self.fields['cantidad_memoria'].widget = forms.HiddenInput()
                self.fields['tipo_memoria'].widget = forms.HiddenInput()
                self.fields['procesador'].required = True
                self.fields['procesador'].widget = forms.Select(attrs={'class': 'form-control'})
                self.fields['valor'].widget = forms.HiddenInput()
            else:
                self.fields['cantidad_memoria'].widget = forms.HiddenInput()
                self.fields['tipo_memoria'].widget = forms.HiddenInput()
                self.fields['procesador'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        caracteristica = cleaned_data.get('caracteristica')
        if caracteristica and caracteristica.nombre == "RAM":
            cantidad = cleaned_data.get('cantidad_memoria')
            tipo = cleaned_data.get('tipo_memoria')
            if cantidad and tipo:
                cleaned_data['valor'] = f"{cantidad.cantidad} {tipo.nombre}"
            else:
                raise forms.ValidationError("Debe seleccionar cantidad y tipo de RAM.")
        elif caracteristica and caracteristica.nombre == "Procesador":
            procesador = cleaned_data.get('procesador')
            if not procesador:
                raise forms.ValidationError("Debe seleccionar un procesador.")
            cleaned_data['valor'] = None  # No usamos valor para procesador
        return cleaned_data

class DispositivoEstadoForm(forms.ModelForm):
    class Meta:
        model = DispositivoEstado
        fields = ['fecha', 'dispositivo_id_dispositivo', 'estado_id_estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dispositivo_id_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'estado_id_estado': forms.Select(attrs={'class': 'form-control'}),
            'agente': forms.HiddenInput(),  # Ocultar agente, se asignará en la vista
        }

class DispositivoUbicacionForm(forms.ModelForm):
    class Meta:
        model = DispositivoUbicacion
        fields = ['fecha', 'dispositivo_id_dispositivo', 'ubicacion_id_ubicacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dispositivo_id_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_id_ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'agente': forms.HiddenInput(),  # Ocultar agente, se asignará en la vista
        }

class DispositivoPropietarioHistoricoForm(forms.ModelForm):
    class Meta:
        model = DispositivoPropietarioHistorico
        fields = ['dispositivo', 'propietario_id_nuevo', 'fecha_cambio']
        widgets = {
            'dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'propietario_id_nuevo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cambio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'agente': forms.HiddenInput(),  # Ocultar agente, se asignará en la vista
        }