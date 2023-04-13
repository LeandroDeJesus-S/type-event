from datetime import datetime
from secrets import token_urlsafe
import csv
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings

from .models import Evento
from .validators import validate_search_by_date, validate_search_date_interval
from utils.validators import (validate_empty_fields, 
                              validate_file_type,
                              validate_start_end_date)


@login_required(redirect_field_name='accounts:login')
def new_events(request):
    if request.method != 'POST':
        return render(request, 'novo_evento.html')
    

    NAME = request.POST.get('nome')
    DESCRIPTION = request.POST.get('descricao')
    START_DATE = request.POST.get('data_inicio')
    END_DATE = request.POST.get('data_termino')
    CARGA_HORARIA = request.POST.get('carga_horaria')

    PRIMARY_COLOR = request.POST.get('cor_principal')
    SECONDARY_COLOR = request.POST.get('cor_secundaria')
    BACKGROUND_COLOR = request.POST.get('cor_fundo')
    
    LOGO = request.FILES.get('logo')
    try:
        validate_empty_fields(NAME, DESCRIPTION, START_DATE, 
                              END_DATE, CARGA_HORARIA, 
                              BACKGROUND_COLOR, LOGO,
                              PRIMARY_COLOR, SECONDARY_COLOR)
        validate_start_end_date(START_DATE, END_DATE)
        validate_file_type(LOGO)
    except Exception as msg:
        msg = list(msg)
        messages.error(request, *msg)
        return redirect('events:new_event')
    
    evento = Evento(
        criador=request.user,
        nome=NAME,
        descricao=DESCRIPTION,
        data_inicio=START_DATE,
        data_termino=END_DATE,
        carga_horaria=CARGA_HORARIA,
        cor_principal=PRIMARY_COLOR,
        cor_secundaria=SECONDARY_COLOR,
        cor_fundo=BACKGROUND_COLOR,
        logo=LOGO,
    )

    evento.save()
    
    messages.success(request, 'Evento cadastrado com sucesso')
    return redirect(reverse('events:new_event'))


@login_required(redirect_field_name='accounts:login')
def manage_event(request):
    eventos = Evento.objects
    context = {'eventos': eventos.filter(criador=request.user)}
    research = request.GET.get('nome')
    
    if research is not None:
        research = validate_search_by_date(research)  # TODO: validar interval
        is_datetime = isinstance(research, datetime)
        if is_datetime:
            context['eventos'] = eventos.filter(
                Q(data_inicio__range=[research, research])|
                Q(data_termino__range=[research, research]), 
                criador=request.user
            )
            
        elif not is_datetime and len(research.split()) > 1:
            interval_dates = validate_search_date_interval(research)
            start_date, end_date = interval_dates
            context['eventos'] = eventos.filter(
                Q(data_inicio__range=[start_date, start_date])|
                Q(data_termino__range=[end_date, end_date]), 
                criador=request.user
            )
        else:
            context['eventos'] = eventos.filter(
                Q(nome__icontains=research)|
                Q(descricao__icontains=research), 
                criador=request.user
            )
            
        
    if request.method == 'GET':
        return render(request, 'gerenciar_evento.html', context)
    

@login_required(redirect_field_name='accounts:login')
def subscribe_event(request, event_id):
    event = get_object_or_404(Evento, id=event_id)
    context = {'evento': event}
    
    if request.method == 'GET':
        return render(request, 'inscrever_evento.html', context)
    
    elif request.method == 'POST':
        if request.user not in event.participantes.all():
            event.participantes.add(request.user)
            event.save()
            messages.success(request, 'Você está participando deste evento!')
        else:
            messages.info(request, 'Você já está participando neste evento!')
            
        return redirect(reverse('events:inscrever_evento', args=[event.pk]))


@login_required(redirect_field_name='accounts:login')
def participants_event(request, event_id):
    if request.method != 'GET':
        pass
    
    event = get_object_or_404(Evento, id=event_id, criador=request.user)
    
    context = {'participantes': event.participantes.all(), 'evento': event}
    return render(request, 'participantes_evento.html', context)


@login_required(redirect_field_name='accounts:login')
def generate_csv(request, id):
    event = get_object_or_404(Evento, id=id, criador=request.user)
    participants = event.participantes.all()

    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)
    
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        for participant in participants:
            x = (participant.username, participant.email)
            writer.writerow(x)
    
    return redirect(f'/media/{token}')
