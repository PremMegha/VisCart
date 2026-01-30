from django.http import JsonResponse

def public_health(request):
    return JsonResponse({"ok": True, "schema": "public"})
