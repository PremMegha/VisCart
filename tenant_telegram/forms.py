from django import forms
from .models import TelegramSettings

class TelegramSettingsForm(forms.ModelForm):
    class Meta:
        model = TelegramSettings
        fields = ["bot_token", "chat_id"]
        widgets = {
            "bot_token": forms.TextInput(attrs={"placeholder": "Telegram Bot Token"}),
            "chat_id": forms.TextInput(attrs={"placeholder": "Telegram Chat ID"}),
        }
