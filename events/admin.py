from django.contrib import admin
from .models import Evento, Certificado

class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criador', 'data_inicio', 'data_termino']

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ['participante', 'evento']

admin.site.register(Evento, EventoAdmin)
admin.site.register(Certificado, CertificadoAdmin)