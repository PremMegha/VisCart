# viscart_cms/public_urls.py
from django.contrib import admin
from django.urls import path

from viscart_cms import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # your public tenants page
    path("tenants/", views.tenant_page, name="tenant_page"),
]
