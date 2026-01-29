from django.db import models

class TelegramSettings(models.Model):
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TelegramSettings(chat_id={self.chat_id})"
