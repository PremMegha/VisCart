from django.contrib import admin
from customers.models import Client, Domain

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "schema_name", "created_on")
    search_fields = ("name", "schema_name")

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("id", "domain", "tenant", "is_primary")
    search_fields = ("domain",)
    list_filter = ("is_primary",)
