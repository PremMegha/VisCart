# viscart/settings_shared.py
from .settings import *  # noqa

# For public/shared migration, we intentionally install ONLY shared apps.
# This guarantees tenant apps like `store` never migrate into public schema.
INSTALLED_APPS = list(SHARED_APPS)

# Public routing (not strictly needed for migration, but keeps things consistent)
PUBLIC_SCHEMA_URLCONF = "viscart.urls_public"
ROOT_URLCONF = "viscart.urls_public"
