from django.shortcuts import render
import pandas as pd
from django.core.paginator import Paginator
from dashboard.models import historial, alerta, perfiles_plantas
import psycopg2
from datetime import datetime, timedelta
from decouple import config
import matplotlib.pyplot as plt
import os
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Consejos
from usuarios.models import usuarios
import random

@login_required
def Dashboard(request):
    last_24_hours = timezone.now() - timedelta(hours=24)
    historial_data = historial.objects.filter(date__gte=last_24_hours).filter(owner_id=request.user)

    # Obtener listas separadas de fechas y humedad
    # dates = [entry.date.strftime("%H:%M") for entry in historial_data]
    dates = [entry.date.astimezone(timezone.get_current_timezone()).strftime("%H:%M") for entry in historial_data]
    humidity = [entry.humidity for entry in historial_data]
    intensity = [entry.intensity for entry in historial_data]
    # for dates in dates:
    #     print(dates)
    ultimo_registro = historial.objects.filter(owner_id=request.user).latest('date')
    nombre_planta = ultimo_registro.planta.plant_name


    # Obtener las últimas 3 alertas del usuario logeado
    user_alertas = alerta.objects.filter(user=request.user).order_by('-id')[:3]

    # Crear una lista para almacenar la información de cada alerta
    alertas_info = []

    # Para cada alerta, obtener los datos relacionados de historial y perfiles_plantas
    for alerta_obj in user_alertas:
        historial_obj = historial.objects.get(id=alerta_obj.id_historial)
        planta_nombre = historial_obj.planta.plant_name
        fecha_alerta = historial_obj.date
        tipo_alerta = alerta_obj.alert
        humedad = historial_obj.humidity
        intensidad = historial_obj.intensity

        # Agregar la información al contexto
        alertas_info.append({
            'fecha_alerta': fecha_alerta,
            'planta_nombre': planta_nombre,
            'tipo_alerta': tipo_alerta,
            'humedad': humedad,
            'intensidad': intensidad
        })

    #Generacion de consejo
    todos_consejos = Consejos.objects.all()
    consejo_aleatorio = random.choice(todos_consejos)
    # listado_usuarios = usuarios.objects.all()


    return render(request, "dashboard.html", {
                        "dates": dates, 
                        "humidity": humidity, 
                        "intensity": intensity, 
                        "ultimo_registro": ultimo_registro, 
                        'alertas_info': alertas_info, 
                        'consejo': consejo_aleatorio,
                        "nombre_planta": nombre_planta
                        })


def Historial(request):

    # media_humedad, media_intensidad = generate_image2()
    plantas = perfiles_plantas.objects.all().values('id', 'plant_name')
    dic_plantas = {planta['id']: planta['plant_name'] for planta in plantas}

    # historial_data = historial.objects.all().values('id', 'date', 'state', 'humidity', 'intensity')
    historial_data = historial.objects.filter(owner_id=request.user).values('id', 'date', 'state', 'humidity', 'intensity', 'owner_id', 'planta_id')
    # crear un dataframe de pandas con los datos obtenidos
    df = pd.DataFrame.from_records(historial_data)
    df['planta_id'] = df['planta_id'].map(dic_plantas)


    #Obtener los valores promedio
    media_humedad = df["humidity"].mean()
    media_intensidad = df["intensity"].mean()

    # formatear la columna 'date' en formato día/mes/año hora:minutos
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y %H:%M')
    # crear un objeto Paginator con los datos del dataframe
    paginator = Paginator(df.values.tolist(), 10)
    # obtener la página solicitada por el usuario
    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
    except:
        page_data = paginator.page(1)

    historial_data = historial.objects.filter(owner_id=request.user)
    dates = [entry.date.astimezone(timezone.get_current_timezone()).strftime("%d/%m %H:%M") for entry in historial_data]
    humidity = [entry.humidity for entry in historial_data]
    intensity = [entry.intensity for entry in historial_data]

    ultimo_registro = historial.objects.filter(owner_id=request.user).latest('date')
    nombre_planta = ultimo_registro.planta.plant_name

    # Obtener las últimas 3 alertas del usuario logeado
    user_alertas = alerta.objects.filter(user=request.user).order_by('-id')[0:]

    # Crear una lista para almacenar la información de cada alerta
    alertas_info = []

    # Para cada alerta, obtener los datos relacionados de historial y perfiles_plantas
    for alerta_obj in user_alertas:
        historial_obj = historial.objects.get(id=alerta_obj.id_historial)
        planta_nombre = historial_obj.planta.plant_name
        fecha_alerta = historial_obj.date
        tipo_alerta = alerta_obj.alert
        humedad = historial_obj.humidity
        intensidad = historial_obj.intensity

        # Agregar la información al contexto
        alertas_info.append({
            'fecha_alerta': fecha_alerta,
            'planta_nombre': planta_nombre,
            'tipo_alerta': tipo_alerta,
            'humedad': humedad,
            'intensidad': intensidad
        })


    return render(request, "historial.html", {
        "page_data": page_data,
        "media_humedad": media_humedad,
        "media_intensidad": media_intensidad,
        "dates": dates, 
        "humidity": humidity, 
        "intensity": intensity,
        "ultimo_registro": ultimo_registro,
        "alertas_info": alertas_info,
        "nombre_planta": nombre_planta
        })


def generate_image2():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Obtener la hora actual
    now = datetime.now()

    # Restar una hora a la hora actual para obtener la hora hace una hora
    one_hour_ago = now - timedelta(hours=1)

    # Formatear las fechas para usarlas en la consulta SQL
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago_formatted = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Consulta SQL para obtener los datos de la última hora
    # consulta = f'SELECT date, humidity, intensity FROM "dashboard_historial" WHERE date BETWEEN \'{one_hour_ago_formatted}\' AND \'{now_formatted}\';'
    # consulta = 'SELECT date, humidity, intensity FROM "dashboard_historial" WHERE CAST(date AS DATE) = CURRENT_DATE;'
    consulta = 'SELECT date, humidity, intensity FROM "dashboard_historial";'

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    media_humedad = df["humidity"].mean()
    media_intensidad = df["intensity"].mean()

    # Convertir la columna 'date' a formato de fecha
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.strftime('%H:%M:%S')
    
    # Graficar los datos
    # plt.figure(figsize=(7, 7))
    # plt.plot(df['time'], df['humidity'], label='Humedad')
    # plt.plot(df['time'], df['intensity'], label='Intensidad')
    # plt.ylabel('Humedad/Intensidad')
    # plt.title('Registro de Medición Humedad e Intensidad')
    # plt.xticks(rotation=45)
    # plt.legend()
    # plt.grid(True)
    # ruta_archivo = 'C:/Users/asana/Desktop/ProyectoApli2/GeniusGreen/GeniusGreen/static/dashboard/plots/mi_grafico2.png'

    # # Verificar si el archivo ya existe
    # if os.path.isfile(ruta_archivo):
    #     # Si el archivo existe, eliminarlo
    #     os.remove(ruta_archivo)

    # # Guardar el gráfico en un archivo
    # plt.savefig(ruta_archivo)

    return (media_humedad, media_intensidad)
    

def User_config(request):

    perfiles = perfiles_plantas.objects.all()

    # Perfil_actual = []

    # # Para cada alerta, obtener los datos relacionados de historial y perfiles_plantas
    # for alerta_obj in user_alertas:
    #     historial_obj = historial.objects.get(id=alerta_obj.id_historial)
    #     planta_nombre = historial_obj.planta.plant_name
    #     fecha_alerta = historial_obj.date
    #     tipo_alerta = alerta_obj.alert
    #     humedad = historial_obj.humidity
    #     intensidad = historial_obj.intensity

    #     # Agregar la información al contexto
    #     Perfil_actual.append({
    #         'fecha_alerta': fecha_alerta,
    #         'planta_nombre': planta_nombre,
    #         'tipo_alerta': tipo_alerta,
    #         'humedad': humedad,
    #         'intensidad': intensidad
    #     })

    return render(request   , "user_config.html", {"perfiles": perfiles})       