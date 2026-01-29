from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    """
    This represents a Tenant.
    Each tenant will have its own PostgreSQL schema.
    """
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # auto-create schema
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    This maps a domain (tenant1.localhost) to a tenant.
    """
    pass
