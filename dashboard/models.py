from django.db import models
from django.contrib.auth.models import User
# from dashboard.models import perfiles_plantas

class perfiles_plantas(models.Model):
    id = models.AutoField(primary_key=True)
    plant_name = models.CharField(max_length=100)
    comentario = models.CharField(default="", max_length=150)
    humidity_excellent = models.IntegerField()
    humidity_regular = models.IntegerField()
    humidity_bad = models.IntegerField()
    intensity_excellent = models.IntegerField()
    intensity_regular = models.IntegerField()
    intensity_bad = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class historial(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default='admin')
    planta = models.ForeignKey(perfiles_plantas, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=30, null=False, default=' ')
    humidity = models.FloatField(null=False, default= 0)
    intensity = models.FloatField(null=False, default=0)

class alerta(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_historial = models.ForeignKey(historial, on_delete=models.CASCADE, default= '1')
    id_historial = models.IntegerField(null=False, default='1')
    alert = models.CharField(max_length=100)

class Consejos(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=100)
    consejo = models.TextField()    

# class ControlPlantas(models.Model):
#     usuario = models.CharField(max_length=255)
#     planta = models.CharField(max_length=255)
#     excelente_luminosidad = models.IntegerField()
#     bien_luminosidad = models.IntegerField()
#     cuidado_luminosidad = models.IntegerField(\)
#     riesgo_luminosidad = models.IntegerField()
#     excelente_humedad = models.IntegerField()
#     bien_humedad = models.IntegerField()
#     cuidado_humedad = models.IntegerField()
#     riesgo_humedad = models.IntegerField()    