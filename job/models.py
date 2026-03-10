from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class OfertaLaboral(models.Model):

    TIPO_EMPLEO = [
        ('TC', 'Tiempo Completo'),
        ('TP', 'Tiempo Parcial'),
        ('CT', 'Contrato'),
        ('RM', 'remoto'),
        ('FR', 'Freelance'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    tipo_empleo = models.CharField(max_length=2, choices=TIPO_EMPLEO)
    descripcion = models.TextField()
    aptitudes = models.CharField(max_length=300)
    metodo_solicitud = models.EmailField()

    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.cargo


class Postulacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.oferta.cargo}"


class Mensaje(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.remitente} a {self.destinatario} sobre {self.oferta}"