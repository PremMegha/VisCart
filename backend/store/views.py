from django.http import JsonResponse
from django.db import connection

def tenant_health(request):
    return JsonResponse({"ok": True, "schema": connection.schema_name})
