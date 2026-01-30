from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # auto-create schema when saving a new tenant
    auto_create_schema = True

    def __str__(self) -> str:
        return f"{self.schema_name} - {self.name}"


class Domain(DomainMixin):
    # DomainMixin already provides:
    # domain, tenant (FK), is_primary
    pass
