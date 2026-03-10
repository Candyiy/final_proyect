from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Habilidad, Servicio, Experiencia, Educacion, Profesion

class RegistroUsuarioForm(UserCreationForm):

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'foto_perfil',
            'password1',
            'password2',
            'telefono',
            'pais',
            'ciudad',
            'nombre',
            'apellidos',
            'fecha_nacimiento',
            'tipo_usuario'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            })

from .models import Empresa

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = [
            'nombre_empresa',
            'nit',
            'direccion',
            'telefono_empresa',
            'pagina_web',
            'descripcion',
            'logo'
        ]

        

class HabilidadForm(forms.ModelForm):

    class Meta:
        model = Habilidad
        fields = ['nombre']
    
class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion']

class ExperienciaForm(forms.ModelForm):

    class Meta:
        model = Experiencia
        fields = [
            'empresa',
            'cargo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'actual'
        ]

class EducacionForm(forms.ModelForm):

    class Meta:
        model = Educacion
        fields = [
            'institucion',
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin'
        ]

class ProfesionForm(forms.ModelForm):

    class Meta:
        model = Profesion
        fields = ['nombre']