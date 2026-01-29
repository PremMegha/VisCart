from django.urls import path
from .views import telegram_settings_view

urlpatterns = [
    path("settings/", telegram_settings_view, name="telegram_settings"),
]
