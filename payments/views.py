import logging
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
import os
from django.views.decorators.http import require_POST
import json

_LOGGER = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def generate_qr_code(request):
    try:
        data = json.loads(request.body)
        if not data:
                return HttpResponseBadRequest('Empty data passed')
        
        amount = data.get('amount', None)
        description = data.get('description', None)
        if not amount or not description or not data:
                return HttpResponseBadRequest('amount and description are not passed')
        
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