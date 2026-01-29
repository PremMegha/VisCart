# viscart_cms/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# CORE
# ------------------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "tenant1.localhost",
    ".localhost",  # allow any subdomain of localhost (tenant routing)
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://tenant1.localhost:8000",
]

# ------------------------------------------------------------------------------
# DJANGO-TENANTS
# ------------------------------------------------------------------------------
INSTALLED_APPS = []  # will be set at bottom

TENANT_MODEL = "customers.Client"   # <-- your tenant model
TENANT_DOMAIN_MODEL = "customers.Domain"  # <-- your domain model

DATABASE_ROUTERS = (
    "django_tenants.routers.TenantSyncRouter",
)

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.environ.get("POSTGRES_DB", "viscart_db"),
        "USER": os.environ.get("POSTGRES_USER", "viscart_admin"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "viscart_password"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# IMPORTANT:
# - public schema should use public_urls
# - tenant schema should use urls.py which includes tenant_urls.py
ROOT_URLCONF = "viscart_cms.urls"
PUBLIC_SCHEMA_URLCONF = "viscart_cms.public_urls"

# ------------------------------------------------------------------------------
# APPS
# ------------------------------------------------------------------------------
SHARED_APPS = (
    "django_tenants",  # must be first
    "customers",       # your tenant + domain models live here

    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # If your public UI needs any custom app:
    "viscart_cms",
)

TENANT_APPS = (
    # django CMS requirements
    "cms",
    "menus",
    "treebeard",
    "sekizai",

    # django CMS media/plugins stack
    "filer",
    "easy_thumbnails",
    "djangocms_text_ckeditor",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_file",
    "djangocms_googlemap",
    "djangocms_video",
    "djangocms_style",
    "djangocms_icon",

    # bootstrap plugins (you had them in migrations)
    # your tenant-specific app(s)
    "tenant_telegram",
)

INSTALLED_APPS = list(SHARED_APPS) + list(TENANT_APPS)

# ------------------------------------------------------------------------------
# MIDDLEWARE (Toolbar needs these)
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # django CMS middleware (order matters)
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

# ------------------------------------------------------------------------------
# TEMPLATES  ✅ THIS IS THE BIG FIX FOR TOOLBAR + CMS
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # <-- make sure templates/ exists
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # django CMS requirements:
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "viscart_cms.wsgi.application"

# ------------------------------------------------------------------------------
# AUTH / I18N
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", "English"),
)

TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

# ------------------------------------------------------------------------------
# STATIC / MEDIA
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# django CMS Templates ✅ REQUIRED
# ------------------------------------------------------------------------------
CMS_TEMPLATES = (
    ("cms_base.html", "CMS Base"),
)

# Optional but recommended
CMS_PERMISSION = True

# ------------------------------------------------------------------------------
# THUMBNAILS (django-filer)
# ------------------------------------------------------------------------------
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
