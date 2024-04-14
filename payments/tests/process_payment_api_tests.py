import json
from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from unittest.mock import patch, MagicMock
from .models import Member, Order, Transaction
from .views import process_payment

class ProcessPaymentAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Member.objects.create(email='customer@example.com', password='password', type='customer')
        self.merchant = Member.objects.create(email='merchant@example.com', password='password', type='merchant')
        self.order = Order.objects.create(member=self.customer, amount=100, status='Created', description='Test order')

    def test_process_payment_success(self):
        url = reverse('process_payment')
        data = {
            'amount': 100,
            'description': 'Test description',
            'customer_id': self.customer.id,
            'merchant_id': self.merchant.id,
            'payment_method': 'credit_card',
            'order_id': self.order.id
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json())
        self.assertEqual(response.json()['message'], 'Payment processed successfully.')
        self.assertTrue('order_id' in response.json())

    def test_process_payment_missing_fields(self):
        url = reverse('process_payment')
        data = {
            'amount': 100,
            'description': 'Test description',
            'customer_id': self.customer.id,
            'merchant_id': self.merchant.id,
            'payment_method': 'credit_card',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_process_payment_invalid_order_id(self):
        url = reverse('process_payment')
        data = {
            'amount': 100,
            'description': 'Test description',
            'customer_id': self.customer.id,
            'merchant_id': self.merchant.id,
            'payment_method': 'credit_card',
            'order_id': 9999,  # Invalid order ID
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_process_payment_exception(self):
        url = reverse('process_payment')
        data = {
            'amount': 100,
            'description': 'Test description',
            'customer_id': self.customer.id,
            'merchant_id': self.merchant.id,
            'payment_method': 'credit_card',
            'order_id': self.order.id
        }
        with patch('payments.views.Transaction.objects.create') as mock_create_transaction:
            mock_create_transaction.side_effect = Exception('Mocked exception')
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 500)
            self.assertTrue('error' in response.json())
