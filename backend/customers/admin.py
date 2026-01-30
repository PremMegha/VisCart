from django.contrib import admin

from viscart.admin_sites import public_admin_site
from .models import Client, Domain


@admin.register(Client, site=public_admin_site)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("schema_name", "name", "created_on")
    search_fields = ("schema_name", "name")


@admin.register(Domain, site=public_admin_site)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")
    search_fields = ("domain",)
    list_filter = ("is_primary",)
