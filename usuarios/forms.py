from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
from .models import usuarios
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields=['username', 'first_name', 'last_name', 'email', 'password1']
    
    cui = forms.IntegerField(label='CUI', help_text='Código Único de Identificación CUI')
    profile_imagen = forms.ImageField(label='Foto de perfil')

    def email_clean(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email = email)  
        if new.count():  
            raise ValidationError("El email ya esta vinculado con otra cuenta, utiliza uno diferente.")  
        return email 
