import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from unittest.mock import patch, MagicMock
from .models import Member, Order, Transaction
from .views import generate_qr_code

class GenerateQRCodeAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.create(email='merchant@example.com', password='password', type='merchant')
        self.customer = Member.objects.create(email='customer@example.com', password='password', type='customer')
        self.order = Order.objects.create(member=self.customer, amount=100, status='Created', description='Test order')

    def test_generate_qr_code_success(self):
        url = reverse('generate_qr_code')
        data = {
            'amount': 100,
            'description': 'Test description',
            'order_id': self.order.id,
            'merchant_id': self.member.id
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('qr_code_url' in response.json())

    def test_generate_qr_code_missing_fields(self):
        url = reverse('generate_qr_code')
        data = {
            'amount': 100,
            'description': 'Test description',
            'order_id': self.order.id,
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_generate_qr_code_invalid_order_id(self):
        url = reverse('generate_qr_code')
        data = {
            'amount': 100,
            'description': 'Test description',
            'order_id': 9999,  # Invalid order ID
            'merchant_id': self.member.id
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    @patch('payments.views.qrcode.make')
    @patch('payments.views.os.path.join')
    def test_generate_qr_code_exception(self, mock_os_path_join, mock_qrcode_make):
        mock_os_path_join.side_effect = Exception('Mocked exception')
        url = reverse('generate_qr_code')
        data = {
            'amount': 100,
            'description': 'Test description',
            'order_id': self.order.id,
            'merchant_id': self.member.id
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
