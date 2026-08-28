from django.http import JsonResponse

from .services import get_leads, get_lead_by_id


def list_leads(request):
    leads = get_leads()

    for lead in leads:
        lead["_id"] = str(lead["_id"])
        lead["created_at"] = lead["created_at"].isoformat()
        lead["updated_at"] = lead["updated_at"].isoformat()

    return JsonResponse(leads, safe=False)

def get_lead(request, lead_id):
    lead = get_lead_by_id(lead_id)

    if lead is None:
        return JsonResponse(
            {"error": "Lead not found"},
            status=404
        )

    lead["_id"] = str(lead["_id"])
    lead["created_at"] = lead["created_at"].isoformat()
    lead["updated_at"] = lead["updated_at"].isoformat()

    return JsonResponse(lead)