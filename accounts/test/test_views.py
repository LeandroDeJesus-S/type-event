from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class TestCadaster(TestCase):
    def test_method_get(self):
        response = self.client.get(reverse('accounts:cadaster'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadaster.html')
        
    def test_user_cadaster_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'senha': 'Testpassword@123',
            'confirmar_senha': 'Testpassword@123'
        }
        response = self.client.post(reverse('accounts:cadaster'), data=data)
        self.assertEqual(response.status_code, 302)
        
        self.assertRedirects(response, reverse('accounts:login'))
        
        user = User.objects.get(username=data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['senha']))
        
    def test_cadaster_empty_fields(self):
        data = {
            'username': '',
            'email': '',
            'senha': '',
            'confirmar_senha': ''
        }
        response = self.client.post(reverse('accounts:cadaster'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:cadaster'))
        
        messages = list(get_messages(response.wsgi_request))
        messages_len = len(list(messages))
        self.assertEqual(messages_len, 1)
        
        for message in messages:
            self.assertIn('Não podem haver campos vazios!', str(message))
    
    def test_username_invalid_cases(self):
        invalid_users = ['user@123', 'usuario_2023', '12345', 'a', '*&']
        data = {
            'username': None,
            'email': 'testuser2@example.com',
            'senha': 'Testpassword@123',
            'confirmar_senha': 'Testpassword@123'
        }
        for user in invalid_users:
            data['username'] = user
            response = self.client.post(reverse('accounts:cadaster'), data)
            messages = list(get_messages(response.wsgi_request))
            for message in messages:
                print(str(message))
                self.assertEqual(
                    'O nome de usuário deve conter apenas letras números e '\
                    'espaços e no mínimo 2 caracteres.', str(message)
                )
        
    def test_cadaster_username_exists(self):
        User.objects.create_user('testuser', 'testuser@example.com', 'Testpassword@123')
        data = {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'senha': 'Testpassword@123',
            'confirmar_senha': 'Testpassword@123'
        }
        response = self.client.post(reverse('accounts:cadaster'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:cadaster'))
        
        messages = list(get_messages(response.wsgi_request))
        messages_len = len(list(messages))
        self.assertEqual(messages_len, 1)
        
        for message in messages:
            self.assertIn('Usuário já existe!', str(message))

    def test_cadaster_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'testuserexample.com',
            'senha': 'Testpassword@123',
            'confirmar_senha': 'Testpassword@123'
        }
        response = self.client.post(reverse('accounts:cadaster'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:cadaster'))
        
        messages = list(get_messages(response.wsgi_request))
        messages_len = len(list(messages))
        self.assertEqual(messages_len, 1)
        
        for message in messages:
            self.assertIn('Informe um endereço de email válido', str(message))

