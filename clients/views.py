from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from events.models import Certificado, Evento
from events.validators import *


def my_certificates(request):
    if request.method == 'GET':
        certificados = Certificado.objects.filter(participante=request.user)
        return render(request, 'meus_certificados.html', {'certificados': certificados})


def my_events(request):
    eventos = Evento.objects
    context = {'eventos': eventos.filter(participantes__username=request.user)}
    research = request.GET.get('nome')
    
    if research is not None:
        research = validate_search_by_date(research)  # TODO: validar interval
        is_datetime = isinstance(research, datetime)
        if is_datetime:
            context['eventos'] = eventos.filter(
                Q(data_inicio__range=[research, research])|
                Q(data_termino__range=[research, research]), 
                participantes__username=request.user
            )
            
        elif not is_datetime and len(research.split()) > 1:
            interval_dates = validate_search_date_interval(research)
            start_date, end_date = interval_dates
            context['eventos'] = eventos.filter(
                Q(data_inicio__range=[start_date, start_date])|
                Q(data_termino__range=[end_date, end_date]), 
                participantes__username=request.user
            )
        else:
            context['eventos'] = eventos.filter(
                Q(nome__icontains=research)|
                Q(descricao__icontains=research), 
                participantes__username=request.user
            )
    
    if request.method == 'GET':
        return render(request, 'meus_eventos.html', context)


def event(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    certificado = get_object_or_404(Certificado, evento__pk=pk)
    context = {'evento': evento, 'certificado': certificado}
    return render(request, 'detalhes_evento.html', context)
