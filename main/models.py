from django.db import models

class consejo(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincrementable
    titulo = models.TextField(default ='Sin titulo', max_length=50, null=False) 
    texto = models.TextField(max_length=150, null=False)  # Campo para almacenar los consejos
    consejo_image = models.ImageField(upload_to='main_consejos', default='main_consejos/default.png')

    class Meta:
        verbose_name= 'consejo'

    def __str__(self):
        return self.titulo

    # def __str__(self):
    #     return self.texto[:50]  # Devuelve los primeros 50 caracteres del consejo


class beneficios_dashboard(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincrementable
    titulo = models.TextField(default ='Sin titulo', max_length=150, null=False) 
    texto = models.TextField(max_length=300, null=False)  # Campo para almacenar los consejos

    class Meta:
        verbose_name= 'Beneficios dashboard'

    def __str__(self):
        return self.titulo

