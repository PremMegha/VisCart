from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import TelegramSettingsForm
from .models import TelegramSettings

def telegram_settings_view(request):
    obj = TelegramSettings.objects.first()  # only one row per tenant

    if request.method == "POST":
        form = TelegramSettingsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Telegram settings saved ✅")
            return redirect("telegram_settings")
    else:
        form = TelegramSettingsForm(instance=obj)

    return render(request, "tenant_telegram/telegram_settings.html", {"form": form})
