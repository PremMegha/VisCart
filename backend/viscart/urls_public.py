from django.urls import path, include
from viscart.admin_sites import public_admin_site

urlpatterns = [
    path("admin/", public_admin_site.urls),
    path("", include("customers.urls")),
]
