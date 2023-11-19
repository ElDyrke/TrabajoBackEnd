from django import forms

from app.models import Cotizacion, Destino, Reserva, Usuario, Viaje

class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class FormDestino(forms.ModelForm):
    class Meta:
        model = Destino
        fields = '__all__'

class FormReserva(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

class FormViaje(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'

class FormCotizacion(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = '__all__'

class FormUsuarioUsername(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id', 'username']
        widgets = {
            'id': forms.HiddenInput(),
        }