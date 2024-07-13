from django import forms
from .models import Categoria, Instrumento, Marca

class InstrumentosForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'disponibilidad', 'marca', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una breve descripción'
            }),
            'precio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Precio del producto'
            }),
            'cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la Cantidad del producto'
            }),
            'disponibilidad': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'marca': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la Marca del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la Categoria del producto'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'imagen': {
                'required': 'Por favor, cargue una imagen para el producto.',
            },
        }

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre de la Marca'
            }),
        }
                
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la nueva Categoria'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una breve descripción'
            }), 
        }