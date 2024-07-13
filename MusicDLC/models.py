from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", null=True)
    
    def __str__(self):
        return f'Instrumento: {self.nombre}, Cantidad Disponibles: {self.cantidad}'
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    nombreCompleto = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    productos = models.ManyToManyField(Instrumento, through='CompraProducto')
    precioFinal = models.DecimalField(max_digits=10, decimal_places=2)
    fechaCompra = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Compra realizada por: {self.usuario.username} el día {self.fechaCompra.date()}"

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    def __str__(self):
        return f"Cliente: {self.compra.nombreCompleto} - Producto: {self.producto.nombre} - {self.cantidad} unidades"