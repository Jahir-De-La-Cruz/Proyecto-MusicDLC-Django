"""
URL configuration for appwebmusic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MusicDLC.views import HomePageView, AddProductsView, LogUsersView, LogoutView, AddMarcaView, AddCategoriaView, GuitarsView, BassView, DrumsView, PianosView, ViolinesView, ConfirmPurchaseView, OrchestraView, SearchProductsView, ContactView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    path('agregar_productos/', AddProductsView.as_view(), name="agregar_productos"),
    path('agregar_marcas/', AddMarcaView.as_view(), name="agregar_marcas"),
    path('agregar_categorias/', AddCategoriaView.as_view(), name="agregar_categorias"),
    path('iniciar_sesion/', LogUsersView.as_view(), name="iniciar_sesion"),
    path('cerrar_sesion/', LogoutView.as_view(), name="cerrar_sesion"),
    path('guitarras/', GuitarsView.as_view(), name="guitarras"),
    path('bajos/', BassView.as_view(), name="bajos"),
    path('baterias/', DrumsView.as_view(), name="baterias"),
    path('teclados/', PianosView.as_view(), name="teclados"),
    path('violines/', ViolinesView.as_view(), name="violines"),
    path('orquesta/', OrchestraView.as_view(), name="orquesta"),
    path('buscar_productos/', SearchProductsView.as_view(), name='buscar_productos'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('confirmar_compra/', ConfirmPurchaseView.as_view(), name="confirmar_compra")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)