from django.db import models

class OfertaLaboral(models.Model):

    TIPO_EMPLEO = [
        ('TC', 'Tiempo Completo'),
        ('TP', 'Tiempo Parcial'),
        ('CT', 'Contrato'),
        ('RM', 'remoto'),
        ('FR', 'Freelance'),
    ]

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

    def __str__(self):
        return self.cargo