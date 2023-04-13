from django.contrib import admin
from .models import Evento

class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criador', 'data_inicio', 'data_termino']

admin.site.register(Evento, EventoAdmin)
