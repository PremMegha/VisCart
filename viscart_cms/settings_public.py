"""
PUBLIC schema settings (NO Django CMS apps)
This file must NOT import viscart_cms.settings with "import *"
because that auto-builds INSTALLED_APPS including tenant apps.
"""

import os
from pathlib import Path

# -----------------------------
# Base / core
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "08#p3jg9#j1z+hl1tt@3g+r1m3#^mtjnejjr2hfm9kh6k$@3xl"
DEBUG = True
ALLOWED_HOSTS = ["*"]

WSGI_APPLICATION = "viscart_cms.wsgi.application"

# -----------------------------
# django-tenants core
# -----------------------------
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"
PUBLIC_SCHEMA_NAME = "public"

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": "viscart_db",
        "USER": "viscart_admin",
        "PASSWORD": "Pm@11@11",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

# -----------------------------
# URLConf: PUBLIC only
# (must not import cms anywhere)
# -----------------------------
ROOT_URLCONF = "viscart_cms.public_urls"
PUBLIC_SCHEMA_URLCONF = "viscart_cms.public_urls"
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

# -----------------------------
# ONLY shared apps (PUBLIC)
# -----------------------------
SHARED_APPS = [
    "django_tenants",
    "customers",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # your public apps
    "viscart_cms",
    "tenant_telegram",
]

INSTALLED_APPS = SHARED_APPS

# -----------------------------
# Middleware (NO CMS middleware here)
# -----------------------------
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# Templates (NO cms context processor)
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "viscart_cms", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.static",
            ],
        },
    },
]

# -----------------------------
# i18n
# -----------------------------
LANGUAGE_CODE = "en"
TIME_ZONE = "Asia/Calcutta"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------
# Static / Media
# -----------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(DATA_DIR, "media")
STATIC_ROOT = os.path.join(DATA_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "viscart_cms", "static"),
)

SITE_ID = 1