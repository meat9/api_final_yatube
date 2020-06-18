from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
]
