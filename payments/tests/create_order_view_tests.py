
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Member, Order
import json

class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            type='customer',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_order_success(self):
        url = reverse('create_order')
        data = {
            'member_id': self.member.id,
            'amount': 100,
            'description': 'Test order'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'order_created'})

    def test_create_order_empty_data(self):
        url = reverse('create_order')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_create_order_invalid_user(self):
        url = reverse('create_order')
        data = {
            'member_id': 999,  # Invalid member ID
            'amount': 100,
            'description': 'Test order'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_order_missing_details(self):
        url = reverse('create_order')
        data = {
            'member_id': self.member.id,
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

