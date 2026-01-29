# viscart_cms/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Tenant-only urls (can safely import cms stuff)
    path("", include("viscart_cms.tenant_urls")),
]
