from django.db import models
from django.conf import settings

# Create your models here.

class Educacion(models.Model):
    titulo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    año_finalizacion = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"
    

