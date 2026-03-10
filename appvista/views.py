from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
#from proyectofront.usuarios.models import Usuario

from usuarios.models import Usuario,Conexion
from job.models import OfertaLaboral, Postulacion, Mensaje
# Create your views here.

from .forms import EducacionForm

@login_required
def home(request):
    ofertas = OfertaLaboral.objects.filter(activa=True).order_by('-fecha_publicacion')
    return render(request, "pages/home.html", {'ofertas': ofertas})

@login_required
def job(request):
    ofertas = OfertaLaboral.objects.filter(usuario=request.user).order_by('-fecha_publicacion')
    return render(request, "pages/job.html", {'ofertas': ofertas})

@login_required
def finalizar_publicacion(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, usuario=request.user)
    if oferta.activa:
        oferta.activa = False
        oferta.save()
        messages.success(request, f'La publicación "{oferta.cargo}" ha sido finalizada. Ya no se aceptan nuevas postulaciones.')
    else:
        messages.warning(request, 'Esta publicación ya está finalizada.')
    return redirect('job')

@login_required
def mensajes(request):
    # Obtener postulaciones aceptadas donde el usuario es el postulante o el propietario de la oferta
    postulaciones_aceptadas = Postulacion.objects.filter(
        (Q(usuario=request.user) | Q(oferta__usuario=request.user)) & Q(status='aceptado')
    ).select_related('usuario', 'oferta').distinct()
    
    # Para cada postulación, obtener los mensajes
    conversaciones = []
    for postulacion in postulaciones_aceptadas:
        mensajes = Mensaje.objects.filter(postulacion=postulacion).order_by('fecha')
        conversaciones.append({
            'postulacion': postulacion,
            'mensajes': mensajes,
            'otro_usuario': postulacion.usuario if postulacion.oferta.usuario == request.user else postulacion.oferta.usuario
        })
    
    context = {
        'conversaciones': conversaciones
    }
    return render(request, "pages/mensajes.html", context)

@login_required
def listapostulantes(request, oferta_id=None):
    if oferta_id:
        # Filtrar postulaciones por oferta específica
        postulaciones = Postulacion.objects.filter(oferta_id=oferta_id).select_related('usuario', 'oferta').prefetch_related(
            'usuario__profesion_set', 'usuario__habilidad_set', 'usuario__servicio_set', 
            'usuario__experiencia_set', 'usuario__educacion_set'
        ).order_by('-fecha')
    else:
        # Mostrar todas las postulaciones
        postulaciones = Postulacion.objects.all().select_related('usuario', 'oferta').prefetch_related(
            'usuario__profesion_set', 'usuario__habilidad_set', 'usuario__servicio_set', 
            'usuario__experiencia_set', 'usuario__educacion_set'
        ).order_by('-fecha')
    
    context = {
        'postulaciones': postulaciones
    }
    return render(request, "pages/listapostulantes.html", context)



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

@login_required
def postular(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    usuario = request.user
    
    if not oferta.activa:
        messages.error(request, 'Esta oferta ya no está disponible para postulaciones.')
        return redirect('home')
    
    # Verificar si el usuario tiene información en su perfil (CV)
    if (usuario.profesion_set.exists() or 
        usuario.habilidad_set.exists() or 
        usuario.servicio_set.exists() or 
        usuario.experiencia_set.exists() or 
        usuario.educacion_set.exists()):
        # Crear la postulación
        Postulacion.objects.create(
            usuario=usuario,
            oferta=oferta
        )
        messages.success(request, 'Postulación enviada exitosamente!')
    else:
        messages.error(request, 'Completa tu perfil (servicios, habilidades, experiencia o educación) antes de postular.')
    
    return redirect('home') 

@login_required
def aceptar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    # Verificar que el usuario sea el propietario de la oferta
    if postulacion.oferta.usuario == request.user:
        postulacion.status = 'aceptado'
        postulacion.save()
        messages.success(request, f'Postulación de {postulacion.usuario.username} aceptada.')
    else:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
    return redirect('lista_postulantes', oferta_id=postulacion.oferta.id)

@login_required
def rechazar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    # Verificar que el usuario sea el propietario de la oferta
    if postulacion.oferta.usuario == request.user:
        postulacion.status = 'rechazado'
        postulacion.save()
        messages.success(request, f'Postulación de {postulacion.usuario.username} rechazada.')
    else:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
    return redirect('lista_postulantes', oferta_id=postulacion.oferta.id)

@login_required
def enviar_mensaje(request, postulacion_id):
    if request.method == 'POST':
        postulacion = get_object_or_404(Postulacion, id=postulacion_id, status='aceptado')
        # Verificar que el usuario participe en la postulación
        if postulacion.usuario == request.user or postulacion.oferta.usuario == request.user:
            contenido = request.POST.get('contenido')
            if contenido:
                # Determinar el destinatario
                destinatario = postulacion.oferta.usuario if postulacion.usuario == request.user else postulacion.usuario
                Mensaje.objects.create(
                    postulacion=postulacion,
                    remitente=request.user,
                    destinatario=destinatario,
                    contenido=contenido
                )
                messages.success(request, 'Mensaje enviado.')
            else:
                messages.error(request, 'El mensaje no puede estar vacío.')
        else:
            messages.error(request, 'No tienes permiso para enviar mensajes en esta conversación.')
    return redirect('mensajes')

