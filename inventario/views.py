from django.shortcuts import render
from inventario.models import articulos
from django.http import HttpRequest
from usuarios.models import usuarios
# Create your views here.

def catalogo(request):
    arts = articulos.objects.all()
    return render(request, "shop.html", {"arts":arts})

def single_product(request, id):
    product = articulos.objects.get(pk=id)
    return render(request, "single-product.html", {"product":product})

def carrito(request):

    return render(request, "cart.html")

def checkout(request):
    info_usuario = usuarios.objects.all()
    pedido_valido = True
    return render(request, "checkout.html", {"info_usuario":info_usuario, "pedido_valido": pedido_valido})