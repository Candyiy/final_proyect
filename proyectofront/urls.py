"""
URL configuration for proyectofront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appvista import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('job/', views.job, name='job'),
    path('mensajes/', views.mensajes, name='mensajes'),
    path('empleos/', include('job.urls')),
    path('listaPostulantes/<int:oferta_id>/', views.listapostulantes, name='lista_postulantes'),
    path('usuariolista/', views.usuariolista, name='usuariolista'),
    path('postular/<int:oferta_id>/', views.postular, name='postular'),
    path('aceptar_postulacion/<int:postulacion_id>/', views.aceptar_postulacion, name='aceptar_postulacion'),
    path('rechazar_postulacion/<int:postulacion_id>/', views.rechazar_postulacion, name='rechazar_postulacion'),
    path('enviar_mensaje/<int:postulacion_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('finalizar_publicacion/<int:oferta_id>/', views.finalizar_publicacion, name='finalizar_publicacion'),

    path('', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
