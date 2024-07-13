from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.core.mail import EmailMessage
from .forms import InstrumentosForm, CategoriaForm, MarcaForm
from .models import Categoria, Instrumento, Marca, Compra, CompraProducto
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminRequiredMixin

# Create your views here.
class HomePageView(View):
    def get(self, request):
        productos = Instrumento.objects.all()[:8]
        return render(request, 'index.html', {
            'productos' : productos
        })

class AddProductsView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        form = InstrumentosForm()
        return render(request, 'agregar_productos.html', {
            'form' : form
        })
        
    def post(self, request):
        try:
            form = InstrumentosForm(request.POST, request.FILES)
            if form.is_valid():
                instrumento = form.save()
                instrumento.save()
                messages.success(request, f'El producto {instrumento.nombre} se agrego correctamente.')
                return redirect('agregar_productos')
            else:
                print(form.errors)
                return render(request, 'agregar_productos.html', {
                    'form' : form,
                    'error' : "Por favor, llene correctamente el formulario"
                })
        except ValueError:
            return render(request, 'agregar_productos.html', {
                'form' : InstrumentosForm(),
                'error' : "Porfavor agregue datos válidos."
            })
            
class ContactView(View):
    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        template = render_to_string('email_template.html', {
            'name' : name,
            'email' : email,
            'subject' : subject,
            'message' : message
        })
        
        email = EmailMessage(subject, template, settings.EMAIL_HOST_USER, ['soyjahirjesua04@gmail.com'])
        
        email.fail_silently = False
        email.send()
        
        messages.success(request, 'Se ha enviado el correo exitosamente!')
        return redirect('home')
            
class AddMarcaView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        form = MarcaForm()
        return render(request, 'agregar_marcas.html', {
            'form' : form
        })
        
    def post(self, request):
        form = MarcaForm(request.POST)
        if form.is_valid():
            form = Marca.objects.create(nombre=request.POST['nombre'])
            form.save()
            if request.user.is_superuser and request.user.is_staff:
                messages.success(request, f'La marca {form.nombre} se agrego correctamente.')
                return redirect('agregar_marcas')
            else:
                return render(request, 'agregar_marcas.html', {
                    'MarcaForm': MarcaForm(),
                    'mensaje' : f'La marca {form.nombre} se agrego correctamente.'
                })
        else:
            return render(request, 'agregar_marcas.html', {
                'form': MarcaForm(),
                'error': 'Por favor, complete correctamente el formulario.'
            })
   
class AddCategoriaView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        form = CategoriaForm()
        return render(request, 'agregar_categorias.html', {
            'form' : form
        }) 
    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form = Categoria.objects.create(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'])
            form.save()
            if request.user.is_superuser and request.user.is_staff:
                messages.success(request, f'La categoria {form.nombre} se agrego correctamente.')
                return redirect('agregar_categorias')
            else:
                return render(request, 'agregar_proveedores.html', {
                    'CategoriaForm' : CategoriaForm(),
                    'mensaje' : f'La categoria {form.nombre} se agrego correctamente.'
                }) 
        else:
            return render(request, 'agregar_proveedores.html', {
                'form': CategoriaForm(),
                'error': 'Por favor, complete correctamente el formulario de categoría.'
            })
   
class LogUsersView(View):
    def get(self, request):
        form_login = AuthenticationForm()
        form_register = UserCreationForm()
        error_message = request.GET.get('error')
        return render(request, 'iniciar_sesion.html', {
            'formLogin': form_login,
            'formRegister': form_register,
            'errorLogin': error_message
        })
        
    def post(self, request):
        form_login = AuthenticationForm()
        form_register = UserCreationForm()

        if 'login' in request.POST:
            form_login = AuthenticationForm(request, request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data['username']
                password = form_login.cleaned_data['password']
                Usuario = authenticate(request, username=username, password=password)
                if Usuario is not None:
                    login(request, Usuario)
                    return redirect('home')
                else:
                    return render(request, 'iniciar_sesion.html', {
                        'formLogin': form_login,
                        'formRegister': form_register,
                        'errorLogin': 'El Usuario ingresado no existe'
                    })
            else:
                return render(request, 'iniciar_sesion.html', {
                    'formLogin': form_login,
                    'formRegister': form_register,
                    'errorLogin': 'Usuario o contraseña incorrectos'
                })
                
        elif 'register' in request.POST:
            form_register = UserCreationForm(request.POST)
            if form_register.is_valid():
                usuario = form_register.save()
                login(request, usuario)
                return redirect('home')
            else:
                return render(request, 'iniciar_sesion.html', {
                    'formLogin': form_login,
                    'formRegister': form_register,
                    'errorRegister': 'Error en el formulario de registro',
                    'registerErrors': form_register.errors
                })

        return render(request, 'iniciar_sesion.html', {
            'formLogin': form_login,
            'formRegister': form_register
        })
        
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
class GuitarsView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(categoria=1)
        return render(request, 'guitarras.html', {
            'productos' : productos
        })
        
class BassView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(categoria=2)
        return render(request, 'bajos.html', {
            'productos' : productos
        })
        
class PianosView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(categoria=3)
        return render(request, 'pianos.html', {
            'productos' : productos
        })

class DrumsView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(categoria=4)
        return render(request, 'baterias.html', {
            'productos' : productos
        })
            
class ViolinesView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(categoria=5)
        return render(request, 'violines.html', {
            'productos' : productos
        })

class OrchestraView(View):
    def get(self, request):
        productos = Instrumento.objects.filter(Q(categoria=6) | Q(categoria=3) | Q(categoria=5))
        return render(request, 'orquesta.html', {
            'productos' : productos
        })
 
class ConfirmPurchaseView(LoginRequiredMixin, View):
    login_url = '/iniciar_sesion/'

    def handle_no_permission(self):
        messages.error(self.request, "Debe iniciar sesión para realizar una compra.")
        return redirect(self.login_url)

    def get(self, request):
        return render(request, 'confirmar_compra.html')

    def post(self, request):
        usuario = request.user
        nombre_comprador = request.POST.get('nombre_comprador')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        productos = request.POST.get('productos').split(',')
        cantidades = request.POST.get('cantidad_productos').split(',')
        precio_final = request.POST.get('precio_final')

        if len(productos) != len(cantidades):
            error = 'La cantidad de productos seleccionados y la cantidad en stock no coinciden!.'
            return render(request, 'confirmar_compra.html', {
                'error': error
            })

        nueva_compra = Compra(usuario=usuario, nombreCompleto=nombre_comprador, email=correo, telefono=telefono, precioFinal=precio_final)
        nueva_compra.save()

        for producto_id, cantidad in zip(productos, cantidades):
            try:
                producto = Instrumento.objects.get(id=producto_id)
            except Instrumento.DoesNotExist:
                error = f'El producto con ID {producto_id} no existe.'
                nueva_compra.delete()
                return render(request, 'confirmar_compra.html', {
                    'error': error
                })
                
            cantidad = int(cantidad)

            if cantidad > producto.cantidad:
                error = f'No hay suficiente stock del producto: "{producto.nombre}"'
                nueva_compra.delete()
                return render(request, 'confirmar_compra.html', {
                    'error': error
                })

            compra_producto = CompraProducto(compra=nueva_compra, producto=producto, cantidad=cantidad)
            compra_producto.save()

            producto.cantidad -= cantidad
            producto.save()

        messages.success(request, "La compra se realizó con éxito!")
        return redirect(reverse('home') + '?success=true')
    
class SearchProductsView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            productos = Instrumento.objects.filter(Q(nombre__icontains=query) | Q(marca__nombre__icontains=query) | Q(categoria__nombre__icontains=query))
        else:
            productos = Instrumento.objects.all()
        return render(request, 'resultado_productos.html', {
            'productos': productos
        })