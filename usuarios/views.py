from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm, EmpresaForm
from django.contrib.auth.decorators import login_required
from .models import Habilidad, Experiencia, Educacion, Servicio, Profesion, Usuario
from .forms import (
    HabilidadForm,
    ServicioForm,
    ExperienciaForm,
    EducacionForm,
    ProfesionForm,
    Empresa
)
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required


def registro(request):
    if request.method == "POST":
        user_form = RegistroUsuarioForm(request.POST, request.FILES)
        empresa_form = EmpresaForm(request.POST, request.FILES)
        
        # Validación según tipo de usuario
        if request.POST.get('tipo_usuario') == "normal":
            # Para persona, solo validamos user_form
            if user_form.is_valid():
                user = user_form.save()
                login(request, user)
                return redirect("home")
        else:
            # Para empresa, validamos ambos
            if user_form.is_valid() and empresa_form.is_valid():
                user = user_form.save()
                empresa = empresa_form.save(commit=False)
                empresa.usuario = user
                empresa.save()
                login(request, user)
                return redirect("home")
        
        # Si llegamos aquí, hay errores en algún formulario
        return render(request, "registro.html", {
            "form": user_form,
            "empresa_form": empresa_form
        })
    
    # GET request
    return render(request, "registro.html", {
        "form": RegistroUsuarioForm(),
        "empresa_form": EmpresaForm()
    })




def login_usuario(request):

    if request.method == 'POST':

        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # verificar si es email
        try:
            user_obj = Usuario.objects.get(email=username_or_email)
            username = user_obj.username
        except Usuario.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            error = "Usuario o contraseña incorrectos"

            return render(request, 'login.html', {
                'error': error
            })

    return render(request, 'login.html')



def cerrar_sesion(request):
    logout(request)
    return redirect('home')



@login_required
def profile(request):

    usuario = request.user

    # EMPRESA
    if usuario.tipo_usuario == "empresa":

        empresa = Empresa.objects.get(usuario=usuario)

        if request.method == "POST":
            empresa_form = EmpresaForm(request.POST, request.FILES, instance=empresa)

            if empresa_form.is_valid():
                empresa_form.save()
                messages.success(request, "Datos de empresa actualizados")
                return redirect("profile")

        else:
            empresa_form = EmpresaForm(instance=empresa)

        return render(request, "usuarios/profileEmpresa.html", {
            "usuario": usuario,
            "empresa_form": empresa_form,
            "empresa": empresa
        })


    # USUARIO NORMAL

    habilidades = Habilidad.objects.filter(usuario=usuario)
    servicios = Servicio.objects.filter(usuario=usuario)
    experiencias = Experiencia.objects.filter(usuario=usuario)
    educaciones = Educacion.objects.filter(usuario=usuario)
    profesiones = Profesion.objects.filter(usuario=usuario)

    habilidad_form = HabilidadForm()
    servicio_form = ServicioForm()
    experiencia_form = ExperienciaForm()
    educacion_form = EducacionForm()
    profesion_form = ProfesionForm()

    if request.method == "POST":

        if "habilidad_submit" in request.POST:

            habilidad_form = HabilidadForm(request.POST)

            if habilidad_form.is_valid():
                habilidad = habilidad_form.save(commit=False)
                habilidad.usuario = usuario
                habilidad.save()

                messages.success(request, "Habilidad guardada")
                return redirect("profile")


        elif "educacion_submit" in request.POST:

            educacion_form = EducacionForm(request.POST)

            if educacion_form.is_valid():
                edu = educacion_form.save(commit=False)
                edu.usuario = usuario
                edu.save()

                messages.success(request, "Educación guardada")
                return redirect("profile")


        elif "servicio_submit" in request.POST:

            servicio_form = ServicioForm(request.POST)

            if servicio_form.is_valid():
                servicio = servicio_form.save(commit=False)
                servicio.usuario = usuario
                servicio.save()

                messages.success(request, "Servicio guardado")
                return redirect("profile")


        elif "experiencia_submit" in request.POST:

            experiencia_form = ExperienciaForm(request.POST)

            if experiencia_form.is_valid():
                experiencia = experiencia_form.save(commit=False)
                experiencia.usuario = usuario
                experiencia.save()

                messages.success(request, "Experiencia guardada")
                return redirect("profile")

    return render(request, "usuarios/profileUsuario.html", {

        "usuario": usuario,

        "habilidades": habilidades,
        "servicios": servicios,
        "experiencias": experiencias,
        "educaciones": educaciones,
        "profesiones": profesiones,

        "habilidad_form": habilidad_form,
        "servicio_form": servicio_form,
        "experiencia_form": experiencia_form,
        "educacion_form": educacion_form,
        "profesion_form": profesion_form,
    })

from django.shortcuts import get_object_or_404
from datetime import datetime

@login_required
def descargar_cv(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    habilidades = Habilidad.objects.filter(usuario=usuario)
    servicios = Servicio.objects.filter(usuario=usuario)
    experiencias = Experiencia.objects.filter(usuario=usuario)
    educaciones = Educacion.objects.filter(usuario=usuario)

    template = get_template("usuarios/cv_pdf.html")

    context = {
        "usuario": usuario,
        "habilidades": habilidades,
        "servicios": servicios,
        "experiencias": experiencias,
        "educaciones": educaciones,
    }

    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")

    anio = datetime.now().year
    nombre = f"{usuario.nombre}_{usuario.apellidos}_{anio}".replace(" ", "_")
    # Cambiado attachment → inline
    response["Content-Disposition"] = f'inline; filename="CV_{nombre}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Usuario, Conexion  # Asegúrate que tienes tu modelo Conexion

@login_required
def enviar_solicitud(request, user_id):
    usuario = request.user
    receptor = get_object_or_404(Usuario, id=user_id)
    Conexion.objects.get_or_create(remitente=usuario, receptor=receptor)
    return redirect("usuariolista")

@login_required
def aceptar_solicitud(request, conexion_id):
    conexion = get_object_or_404(Conexion, id=conexion_id, receptor=request.user)
    conexion.aceptada = True
    conexion.save()
    return redirect("usuariolista")

@login_required
def rechazar_solicitud(request, conexion_id):
    conexion = get_object_or_404(Conexion, id=conexion_id, receptor=request.user)
    conexion.aceptada = False
    conexion.save()
    return redirect("usuariolista")

@login_required
def eliminar_item(request, tipo, id):

    usuario = request.user

    modelos = {
        "habilidad": Habilidad,
        "servicio": Servicio,
        "experiencia": Experiencia,
        "educacion": Educacion,
    }

    modelo = modelos.get(tipo)

    if modelo:
        item = get_object_or_404(modelo, id=id, usuario=usuario)
        item.delete()
        messages.success(request, f"{tipo.capitalize()} eliminada")

    return redirect("profile")