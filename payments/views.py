import logging
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import qrcode
import os
from django.views.decorators.http import require_POST
import json

from payments.models import Order, Transaction, Member

_LOGGER = logging.getLogger(__name__)

# customer places an order
@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
        if not data:
                return HttpResponseBadRequest('Empty data passed')
        member_id = data.get('member_id')
        amount = data.get('amount')
        description = data.get('description')
        member_instance = Member.objects.get(pk=member_id)

        if not member_id or not member_instance:
             return HttpResponseBadRequest('Invalid user')
        if not amount and not description:
             return HttpResponseBadRequest('Missing Order details')

        Order.objects.create(
            member=member_instance,
            amount=amount,
            status='Created',
            description=description
        )
        response_data = {'message': 'order_created'}
        return JsonResponse(response_data, status=201)
    except Exception as error:
        _LOGGER.error('Error in create_order API')
        raise error   

# qr will be generated by merchant for an order
@csrf_exempt
@require_POST
def generate_qr_code(request):
    try:
        data = json.loads(request.body)
        if not data:
                return HttpResponseBadRequest('Empty data passed')
        
        amount = data.get('amount', None)
        description = data.get('description', None)
        order_id = data.get('order_id', None)
        merchant_id = data.get('merchant_id', None)
        if not all([amount, description, order_id, merchant_id]):
            return HttpResponseBadRequest('amount, description, order_id, and merchant_id are required')
        
        order = get_object_or_404(Order, id=order_id)
        
        transaction = Transaction.objects.create(
            from_member_id=merchant_id,
            to_member_id=order.member.id,
            order=order,
            amount=amount,
            status='Initiated',
            payment_method=None
        )
        transaction.save()
        
        payment_details = f"Amount: {amount}, Description: {description}"
        qr = qrcode.make(payment_details)
        qr_filename = 'qr_code.png'
        qr_path = os.path.join(settings.STATICFILES_DIRS[0], qr_filename)
        qr.save(qr_path)
        qr_url = os.path.join(settings.STATIC_URL, qr_filename)      

        return JsonResponse({'qr_code_url': qr_url})
    except Exception as error:
        _LOGGER.error('Error in generate_qr_code API')
        raise error
    
# payment is done by customer for his placed order
@csrf_exempt
@require_POST
def process_payment(request):
    try:
        data = json.loads(request.body)
        if not data:
                return HttpResponseBadRequest('Empty data passed')
        amount = data.get('amount', None)
        description = data.get('description', None)
        customer = data.get('customer_id', None)
        merchant_id = data.get('merchant_id', None)
        payment_method = data.get('payment_method', None)
        order_id = data.get('order_id', None)

        if not all([amount, description, customer, merchant_id, payment_method, order_id]):
            return HttpResponseBadRequest('amount, description, customer_id, merchant_id,  payment_method, and order_id are required')
        
        transaction = None
        order = get_object_or_404(Order, id=order_id)

        # user id to be fetched from request header or cookies
        transaction = Transaction.objects.create(
            from_member_id=customer,
            to_member_id=merchant_id,
            order=order,
            amount=amount,
            status='Completed',
            payment_method=payment_method
        )
        return JsonResponse({'message': 'Payment processed successfully.', 'order_id': order_id})
    except Exception as e:
        if transaction:
            transaction.status = 'Failed'
            transaction.save()
        return JsonResponse({'error': str(e)}, status=500)
