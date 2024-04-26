from django.contrib import admin
from .models import consejo, beneficios_dashboard
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class serviciosresource(resources.ModelResource):
    fields =('id', 'titulo', 'texto', 'consejo_image')
    
    class Meta:
        model = consejo

@admin.register(consejo)
class ServiciosAdmin(ImportExportModelAdmin):
    resource_class = serviciosresource
    # readonly_fields=('id')
    list_display = ['id', 'titulo', 'texto'] #Propiedades visibles del campo
    # list_filter=['categoria', 'disponibilidad']  #Añadir buscar por filtro
    list_per_page=15    #Cantidad de items por pagina
    # list_editable=['disponibilidad',]


@admin.register(beneficios_dashboard)
class ServiciosAdmin(ImportExportModelAdmin):
    resource_class = serviciosresource
    # readonly_fields=('id')
    list_display = ['id', 'titulo', 'texto'] #Propiedades visibles del campo
    # list_filter=['categoria', 'disponibilidad']  #Añadir buscar por filtro
    list_per_page=15    #Cantidad de items por pagina
    # list_editable=['disponibilidad',]