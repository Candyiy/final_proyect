from django.urls import path
from . import views
from .models import Usuario, Conexion
urlpatterns = [

    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path("profile/", views.profile, name="profile"),
    path("enviar/<int:user_id>/", views.enviar_solicitud, name="enviar_solicitud"),
    path("aceptar/<int:conexion_id>/", views.aceptar_solicitud, name="aceptar_solicitud"),
    path("rechazar/<int:conexion_id>/", views.rechazar_solicitud, name="rechazar_solicitud"),
    path("cv/<int:user_id>/", views.descargar_cv, name="descargar_cv"),
]