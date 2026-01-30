from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group


class PublicAdminSite(AdminSite):
    site_header = "VisCart Public Admin"
    site_title = "VisCart Public Admin"
    index_title = "Tenant Management"


class TenantAdminSite(AdminSite):
    site_header = "VisCart Tenant Admin"
    site_title = "VisCart Tenant Admin"
    index_title = "Store Management"


public_admin_site = PublicAdminSite(name="public_admin")
tenant_admin_site = TenantAdminSite(name="tenant_admin")

# Register auth models on PUBLIC admin (recommended)
User = get_user_model()
public_admin_site.register(User, UserAdmin)
public_admin_site.register(Group, GroupAdmin)
