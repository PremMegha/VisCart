from django.urls import path, include
from viscart.admin_sites import tenant_admin_site

urlpatterns = [
    path("admin/", tenant_admin_site.urls),
    path("", include("store.urls")),
]
