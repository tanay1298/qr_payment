from django.urls import path
from payments.views import create_order, generate_qr_code, process_payment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-order/', create_order, name='create_order'),
    path('generate-qr-code/', generate_qr_code, name='generate_qr_code'),
    path('process-payment/', process_payment, name='process_payment'),
]


# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
