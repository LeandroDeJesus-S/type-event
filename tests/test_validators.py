from utils import validators
from django.test import TestCase
from unittest.mock import patch, Mock
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

class TestValidators(TestCase):
    def setUp(self) -> None:
        self.user_target = 'utils.validators.User'
        
        self.fake_queryset_to_valid_cases = Mock(spec=QuerySet)
        self.fake_queryset_to_valid_cases.exists.return_value = False  # obj not exists
        
        self.fake_queryset_to_invalid_cases = Mock(spec=QuerySet)
        self.fake_queryset_to_invalid_cases.exists.return_value = True  # obj exists
        
        self.fake_user_to_valid_cases = Mock()
        self.fake_user_to_valid_cases.objects.filter.return_value = self.fake_queryset_to_valid_cases
        
        self.fake_user_to_invalid_cases = Mock()
        self.fake_user_to_invalid_cases.objects.filter.return_value = self.fake_queryset_to_invalid_cases
    
    def test_validate_username_with_valid_entries(self):
        entries = [
            'teste', 'Teste123', 'TESTE', 'tEStE 122'
        ]
        for entry in entries:
            with self.subTest(entry=entry):
                validators.validate_username(entry)
                
    def test_validate_username_with_invalid_entries(self):
        entries = [
            '123', 'Teste_123', 'TESTE@123', '@1#$'
        ]
        for entry in entries:
            with self.subTest(entry=entry):
                self.assertRaises(
                    ValidationError,
                    validators.validate_username,
                    entry
                )
    
    def test_validate_username_exists_with_new_user(self):
        with patch(self.user_target, self.fake_user_to_valid_cases):
            result = validators.validate_user_exists('new user')
            self.assertIsNone(result)
    
    def test_validate_username_exists_with_existing_user(self):
        with patch(self.user_target,self.fake_user_to_invalid_cases):
            with self.assertRaises(ValidationError):
                validators.validate_user_exists('user_existente')
    
    def test_validate_email_pattern(self):
        valid_email_tests = 'test@example.com', 'teste@email.me'
        invalid_email_tests = 't@email', '@email.com', 'test@'
        valid_and_invalid_emails = zip(valid_email_tests, invalid_email_tests)
        
        for valid_email, invalid_email in valid_and_invalid_emails:
            with self.subTest(valid_email=valid_email):
                self.assertIsNone(
                    validators.validate_email_pattern(valid_email)
                )
                
            with self.subTest(invalid_email=invalid_email):
                self.assertRaises(
                    ValidationError,
                    validators.validate_email_pattern,
                    invalid_email
                )
    
    def test_validate_email_with_new_email(self):
        email_test = 'test@example.com'
        with patch(self.user_target, self.fake_user_to_valid_cases):
            result = validators.validate_email_exists(email_test)
            self.assertIsNone(result) 
            
    def test_validate_email_with_existing_email(self):
        with patch(self.user_target, self.fake_user_to_invalid_cases):
            with self.assertRaises(ValidationError):
                email_test = 'exitingEmail@example.com'
                validators.validate_email_exists(email_test)          
                  
    def test_validate_email_with_valid_entry(self):
        email_test = 'test@example.com'
        result = validators.validate_email_exists(email_test)
        self.assertIsNone(result)           
        
    def test_validate_password_strong_with_valid_entries(self):
        entries = [
            'Teste@123', 'tesTe_123', 'cTESTE*123', 'T3st3@1234'
        ]
        for entry in entries:
            with self.subTest(entry=entry):
                validators.validate_password_strong(entry)
                
    def test_validate_password_strong_with_invalid_entries(self):
        entries = [
            'teste1234', 'Teste@#$@', 'Teste()123', 'TESTE@1#$'
        ]
        for entry in entries:
            with self.subTest(entry=entry):
                self.assertRaises(
                    ValidationError,
                    validators.validate_password_strong,
                    entry
                )

    def test_validate_password_confirmation(self):
        valid_case = 'Teste@1234', 'Teste@1234'
        invalid_case = 'Teste@1234', 'Teste@123'
        
        self.assertIsNone(
            validators.validate_password_confirmation(*valid_case)
        )
        self.assertRaises(ValidationError, 
                          validators.validate_password_confirmation, 
                          *invalid_case)

    def test_validate_start_end_date(self):
        valid_case = '2023-03-01', '2023-03-02'
        invalid_case = '2023-03-02', '2023-03-01'
        
        self.assertIsNone(validators.validate_start_end_date(*valid_case))
        with self.assertRaises(ValidationError):
            validators.validate_start_end_date(*invalid_case)
    
    def test_validate_hexadecimal_color(self):
        valid_cases = "#FFAABB", '#ffffff', '#bf093d', '#c1bd48'
        invalid_cases = '#GG0000', '#12345', '00#00FF', '#00FF00FF'
        
        for valid_case, invalid_case in zip(valid_cases, invalid_cases):
            with self.subTest(valid_case=valid_case):
                self.assertIsNone(
                    validators.validate_hexadecimal_color(valid_case)
                )
                self.assertRaises(
                    ValidationError, 
                    validators.validate_hexadecimal_color,
                    invalid_case
                )
        
        