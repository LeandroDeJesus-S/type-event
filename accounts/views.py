from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

from utils import validators

def cadaster(request):
    if request.method != 'POST':
        return render(request, 'cadaster.html')
    
    USERNAME = request.POST.get('username')
    EMAIL = request.POST.get('email')
    PASSWORD = request.POST.get('senha')
    PASSWORD_CONFIRM = request.POST.get('confirmar_senha')
    
    try:
        validators.validate_empty_fields(USERNAME, EMAIL, 
                                         PASSWORD, PASSWORD_CONFIRM)
        validators.validate_username(USERNAME)
        validators.validate_user_exists(USERNAME)
        validators.validate_email_pattern(EMAIL)
        validators.validate_email_exists(EMAIL)
        validators.validate_password_strong(PASSWORD)
        validators.validate_password_confirmation(PASSWORD, PASSWORD_CONFIRM)
    except Exception as msg:
        msg = list(msg)
        messages.error(request, *msg)
        return redirect(reverse('accounts:cadaster'))
        
    user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
    
    return redirect(reverse('accounts:login'))


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    
    USERNAME = request.POST.get('username')
    PASSWORD = request.POST.get('senha')
    
    user = auth.authenticate(username=USERNAME, password=PASSWORD)
    
    if user is None:
        messages.error(request, 'Usuário ou senha incorretos!')
        return redirect(reverse('accounts:login'))
    
    auth.login(request, user=user)
    return redirect(reverse('events:new_event'))