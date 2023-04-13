from unittest.mock import MagicMock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core. exceptions import ValidationError

from ..models import Evento

class TestEvento(TestCase):
    def setUp(self) -> None:
        self.user = MagicMock(User)
        self.user.username='Test123'
        self.user.email='Test123@example.com',
        self.user.password='Password@123'

        self.evento = MagicMock(Evento)
        self.evento.criador = self.user
        self.evento.nome='Meu evento'
        self.evento.descricao='Descrição do meu evento'
        self.evento.data_inicio='2023-01-01'
        self.evento.data_termino='2023-01-02'
        self.evento.carga_horaria=8
        self.evento.cor_principal='#FF0000'
        self.evento.cor_secundaria='#00FF00'
        self.evento.cor_fundo='#0000FF'
        
    def test_evento_criado_corretamente(self):
        self.assertEqual(self.evento.criador, self.user)
        self.assertEqual(self.evento.nome, 'Meu evento')
        self.assertEqual(self.evento.descricao, 'Descrição do meu evento')
        self.assertEqual(self.evento.data_inicio, '2023-01-01')
        self.assertEqual(self.evento.data_termino, '2023-01-02')
        self.assertEqual(self.evento.carga_horaria, 8)
        self.assertEqual(self.evento.cor_principal, '#FF0000')
        self.assertEqual(self.evento.cor_secundaria, '#00FF00')
        self.assertEqual(self.evento.cor_fundo, '#0000FF')
           