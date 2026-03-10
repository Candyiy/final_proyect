from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from proyectofront.usuarios.models import Usuario

from usuarios.models import Usuario,Conexion
# Create your views here.

from .forms import EducacionForm
from job.models import OfertaLaboral

@login_required
def home(request):
    ofertas = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    return render(request, "pages/home.html", {'ofertas': ofertas})

@login_required
def job(request):
    ofertas = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    return render(request, "pages/job.html", {'ofertas': ofertas})

@login_required
def mensajes(request):
    return render(request, "pages/mensajes.html")

@login_required
def listapostulantes(request):
    return render(request, "pages/listapostulantes.html")



@login_required
def usuariolista(request):
    usuarios = Usuario.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    # Solicitudes enviadas por mí
    solicitudes_enviadas = set(
        Conexion.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    )
    # Solicitudes pendientes que me llegaron
    solicitudes_recibidas = Conexion.objects.filter(to_user=request.user, status='pendiente')

    context = {
        "usuarios": usuarios,
        "solicitudes_enviadas": solicitudes_enviadas,
        "solicitudes_recibidas": solicitudes_recibidas
    }
    return render(request, "pages/usuariolista.html", context)



