from django.http import JsonResponse

from .services import get_leads


def list_leads(request):
    leads = get_leads()

    for lead in leads:
        lead["_id"] = str(lead["_id"])
        lead["created_at"] = lead["created_at"].isoformat()
        lead["updated_at"] = lead["updated_at"].isoformat()

    return JsonResponse(leads, safe=False)