from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
import os

@csrf_exempt
def generate_qr_code(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        
        qr = qrcode.make(f"Amount: {amount}, Description: {description}")
        qr_filename = 'qr_code.png'
        qr_path = os.path.join(settings.STATICFILES_DIRS[0], qr_filename)
        qr.save(qr_path)
        qr_url = os.path.join(settings.STATIC_URL, qr_filename)

        return JsonResponse({'qr_code_url': qr_url})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
