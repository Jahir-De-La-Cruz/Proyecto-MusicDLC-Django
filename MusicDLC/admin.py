from django.contrib import admin
from .models import Categoria, Instrumento, Marca, CompraProducto, Compra

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Instrumento)
admin.site.register(Marca)
admin.site.register(CompraProducto)
admin.site.register(Compra)