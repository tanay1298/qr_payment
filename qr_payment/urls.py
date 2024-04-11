from django.urls import path
from payments.views import generate_qr_code
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('generate-qr-code/', generate_qr_code, name='generate_qr_code'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
