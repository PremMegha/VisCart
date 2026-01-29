# viscart_cms/tenant_urls.py
from cms.sitemaps import CMSSitemap
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
]
