from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import consejo, beneficios_dashboard
from inventario.models import articulos
from carro.carro import Carro

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def Home(request):
    carro = Carro(request)
    arts = articulos.objects.all()

    ultimos_articulos=[]

    if len(arts)>3:
        for i in range(len(arts)-3, len(arts)):
            ultimos_articulos.append(arts[i])
    else:
        for i in range(0, len(arts)):
            ultimos_articulos.append(arts[i])

    return render(request, "home.html", {"arts":arts, "articulos":ultimos_articulos})

def DashboardInfo(request):
    beneficio = beneficios_dashboard.objects.all()

    return render(request, "dashboard_info.html", {"beneficio": beneficio})    

def Login(request):

    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario = authenticate(request=request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                # reset(username=username)
                return redirect('Home')
            else:
                messages.error(request,"Usuario no válido")
        else:
            messages.error(request,"Información no válida")

    form = AuthenticationForm()
    return render(request, "signin.html", {"form":form})    

def FAQs(request):
    consejos = consejo.objects.all()

    return render(request, "FAQs.html", {"consejo": consejos})

def Contacto(request):

    return render(request, "contacto.html")       

def cerrar_sesion(request):
    logout(request)
    return redirect('Home')