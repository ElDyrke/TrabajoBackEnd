from django.db import models

# Create your models here.
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    username = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=10)
    apellido = models.CharField(max_length=50)
    contrasenna = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Destino(models.Model):
    nombre = models.CharField(max_length=50)
    html_src = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

class Viaje(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=144)
    stock = models.IntegerField()
    precio = models.IntegerField()
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Cotizacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    viajes = models.ManyToManyField(Viaje, related_name="cotizaciones")
    fecha_minima = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_maxima = models.DateTimeField(auto_now=False, auto_now_add=False)

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    fecha_ida = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_vuelta = models.DateTimeField(auto_now=False, auto_now_add=False)   

    def __str__(self):
        return self.nombre 