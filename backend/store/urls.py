from django.urls import path
from .views import tenant_health

urlpatterns = [
    path("health/", tenant_health),
]
