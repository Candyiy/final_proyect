from django.contrib import admin
from .models import Habilidad, Profesion, Usuario, Experiencia, Educacion, Servicio,Empresa

admin.site.register(Usuario)

admin.site.register(Habilidad)
admin.site.register(Experiencia)
admin.site.register(Educacion)
admin.site.register(Servicio)