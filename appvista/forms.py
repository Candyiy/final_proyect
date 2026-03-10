from django import forms
from .models import Educacion

class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'año_finalizacion', 'descripcion']