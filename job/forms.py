from django import forms
from .models import OfertaLaboral

class OfertaForm(forms.ModelForm):

    class Meta:
        model = OfertaLaboral
        fields = [
            'cargo',
            'empresa',
            'ubicacion',
            'tipo_empleo',
            'descripcion',
            'aptitudes',
            'metodo_solicitud',
            'fecha_inicio',
            'fecha_fin'
        ]

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':5}),
            'aptitudes': forms.TextInput(attrs={'placeholder':'Python, Django, SQL'}),
            'fecha_inicio': forms.DateInput(attrs={'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'type':'date'}),
        }