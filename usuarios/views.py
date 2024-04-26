from django.views.generic import ListView, View
from unicodedata import name
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .utils import render_to_pdf
from .forms import CustomUserCreationForm  
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import itertools
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
# from axes.utils import reset

from .models import usuarios
from pedidos.models import LineaPedido, Pedido
# from usuarios.models import usuarios
from inventario.models import articulos

from .utils import render_to_pdf


from django.contrib.auth import get_user_model
User = get_user_model()

class VRegistro(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registro.html", {"form":form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.save()
            ncui = form.cleaned_data.get('cui')
            img = form.cleaned_data.get("profile_imagen")
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            usuario = authenticate(request=request, username=username, password=password)
            login(request, usuario)

            nuevo_usuario = usuarios(user=request.user, username=request.user.username, fisrt_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email, cui=ncui, profile_image = img)
            nuevo_usuario.save()

            return redirect('Home')
        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            return render(request, "registro.html", {"form":form})

def perfil(request):

    articulos_comprados = LineaPedido.objects.all()
    pedidos_comprados = Pedido.objects.all()
    listado_todos_productos = articulos.objects.all()
    listado_usuarios = usuarios.objects.all()

    return render(request, "perfil.html", {
                        "articulos_comprados":articulos_comprados, 
                        "listado_todos_productos":listado_todos_productos, 
                        'listado_usuarios': listado_usuarios, 
                        'pedidos_comprados': pedidos_comprados
                        })

class perfil_pdf(View):
    # model= LineaPedido
    # template_name= "perfil/perfil.html"
    # context_object_name = 'articulos_comprados'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)    
    #     context['listado_todos_productos'] = articulos.objects.all()
    #     return context
    def get(self, request, *arg, **kwargs):
        user_id = request.user.id
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

        user={
            'id':user_id,
            'username': username,
            'first_name':first_name,
            'last_name': last_name,
            'email': email
        }

        # print(user["username"])
        
        # articulos_comprados = LineaPedido.objects.get(user_id=user_id)
        articulos_comprados = LineaPedido.objects.all()
        listado_todos_productos = articulos.objects.all()
        pedidos_comprados = Pedido.objects.all()
        # print(articulos_comprados)

        articulos_comprados2=[]
        listado_todos_productos2=[]
        for articulos_comprados in articulos_comprados:
            # print(articulos_comprados.producto)
            if articulos_comprados.user_id == user_id:
                articulos_comprados2.append(articulos_comprados)
                articulo = articulos.objects.get(pk=articulos_comprados.producto_id)
                listado_todos_productos2.append(articulo)
        data={
            'articulos_comprados': articulos_comprados2,
            'listado_todos_productos': listado_todos_productos,
            'pedidos_comprados': pedidos_comprados,
            'user': user
        }
        pdf = render_to_pdf('perfil_pdf.html', data)
        # print(articulos_comprados2)
        
        return HttpResponse(pdf, content_type='application/pdf')