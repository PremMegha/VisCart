import logging
import os
import requests
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_client_telegram_config():
    """
    Return (bot_token, chat_id) for the current tenant Client.
    If we're in public/shell context (FakeTenant), return (None, None).
    Optional fallback: allow env vars for manual testing.
    """
    tenant = getattr(connection, "tenant", None)

    bot_token = getattr(tenant, "telegram_bot_token", None)
    chat_id = getattr(tenant, "telegram_chat_id", None)

    # If tenant doesn't have fields (FakeTenant/public), fallback to env for testing only
    if not bot_token or not chat_id:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

    return bot_token, chat_id


def send_telegram(message: str) -> None:
    bot_token, chat_id = _get_client_telegram_config()

    if not bot_token or not chat_id:
        logger.warning("Telegram not configured (tenant fields or env vars missing).")
        return

    schema = getattr(connection, "schema_name", settings.PUBLIC_SCHEMA_NAME)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"Tenant: <b>{schema}</b>\n\n{message}",
        "parse_mode": "HTML",
    }

    try:
        resp = requests.post(url, json=payload, timeout=7)
        resp.raise_for_status()
    except Exception as exc:
        logger.exception("Telegram send failed: %s", exc)
