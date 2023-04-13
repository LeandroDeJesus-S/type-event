import re
import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, FileExtensionValidator


def validate_empty_fields(*fields):
    for field in fields:
        if field is None:
            raise ValidationError('Não podem haver campos vazios!')


def validate_username(username):
    regex = re.compile(r'^(?!^\d+$)[a-zA-Z0-9\s]+$')
    if not regex.search(username):
        msg = 'O nome de usuário deve conter apenas letras números e espaços'
        raise ValidationError(msg)


def validate_user_exists(username):
    verifying = User.objects.filter(username=username).exists()
    if verifying:
        raise ValidationError('Usuário já existe!')


def validate_email_pattern(email):
    return validate_email(email)


def validate_email_exists(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('E-mail já existe!')


def validate_password_strong(password):
    regex = re.compile(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*-_])[A-Za-z\d!@#$%^&*-_]{8,}$'
    )
    if not regex.search(password):
        msg = 'A senha precisa ter no mínimo 1 letra maiúscula, 1 minuscula '\
              '1 número, 1 simbolo entre "!@#$%^&*-_" e no mínimo 8 caracteres'
        raise ValidationError(msg)


def validate_password_confirmation(pw, pw_confirm):
    if pw != pw_confirm:
        raise ValidationError('As senhas não coincidem!')
    
    
def validate_start_end_date(start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    if start > end:
        raise ValidationError('Datas de inicio e término inválidas!')


def validate_file_type(file):
    available_types = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'svg']
    return FileExtensionValidator(
        available_types, 
        f'Tipo de arquivo inválido! os tipos suportados são: {available_types}'
    ).__call__(file)


def validate_hexadecimal_color(color: str):
    regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if not regex.search(color):
        raise ValidationError('Cor inválida!')
