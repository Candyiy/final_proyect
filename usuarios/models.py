from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class Usuario(AbstractUser):

    telefono = models.CharField(max_length=20, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True, default='perfiles/perfil.png')
    email = models.EmailField()

    pais = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    fecha_nacimiento = models.DateField(null=True, blank=True)

    TIPO_USUARIO = (
        ('normal', 'Usuario'),
        ('admin', 'Administrador'),
        ('empresa', 'Empresa'),
    )

    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO, default='normal')

    def __str__(self):
        return self.username

class Empresa(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=200)
    nit = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono_empresa = models.CharField(max_length=20)
    pagina_web = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='empresas/', blank=True, null=True, default='perfiles/logo.png')

    def __str__(self):
        return self.nombre_empresa
    
class Profesion(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    
class Habilidad(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=100)

    nivel = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.nombre
    
class Servicio(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=200)

    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Experiencia(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    empresa = models.CharField(max_length=200)

    cargo = models.CharField(max_length=200)

    descripcion = models.TextField(blank=True)

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(null=True, blank=True)

    actual = models.BooleanField(default=False)

    def __str__(self):
        return self.cargo
    
class Educacion(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    institucion = models.CharField(max_length=200)

    titulo = models.CharField(max_length=200)

    descripcion = models.TextField(blank=True)

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo
    



class Conexion(models.Model):
    from_user = models.ForeignKey(
        Usuario, 
        related_name='conexiones_enviadas', 
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        Usuario, 
        related_name='conexiones_recibidas', 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, 
        choices=(('pendiente', 'Pendiente'), ('aceptada', 'Aceptada')), 
        default='pendiente'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"


