from django.urls import path
from .views import public_health

urlpatterns = [
    path("health/", public_health),
]
