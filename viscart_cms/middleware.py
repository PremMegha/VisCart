from django.db import connection

from cms.middleware.utils import ApphookReloadMiddleware
from cms.middleware.user import CurrentUserMiddleware
from cms.middleware.page import CurrentPageMiddleware
from cms.middleware.toolbar import ToolbarMiddleware
from cms.middleware.language import LanguageCookieMiddleware


class TenantOnlyCMSMiddleware:
    """
    Runs Django CMS middlewares ONLY for tenant schemas.
    Avoids public schema querying CMS tables (cms_urlconfrevision etc).
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # instantiate CMS middleware chain (in same order you had)
        self._cms_middlewares = [
            ApphookReloadMiddleware(get_response),
            CurrentUserMiddleware(get_response),
            CurrentPageMiddleware(get_response),
            ToolbarMiddleware(get_response),
            LanguageCookieMiddleware(get_response),
        ]

    def __call__(self, request):
        # Skip CMS middleware on public schema
        if connection.schema_name == "public":
            return self.get_response(request)

        # Run CMS middlewares process_request
        for mw in self._cms_middlewares:
            if hasattr(mw, "process_request"):
                response = mw.process_request(request)
                if response:
                    return response

        response = self.get_response(request)

        # Run CMS middlewares process_response (reverse order)
        for mw in reversed(self._cms_middlewares):
            if hasattr(mw, "process_response"):
                response = mw.process_response(request, response)

        return response
