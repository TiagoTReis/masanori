import json

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .services import create_lead, get_leads, get_lead_by_id


@csrf_exempt
def list_leads(request):
    if request.method == "GET":
        leads = get_leads()

        for lead in leads:
            lead["_id"] = str(lead["_id"])
            lead["created_at"] = lead["created_at"].isoformat()
            lead["updated_at"] = lead["updated_at"].isoformat()

        return JsonResponse(leads, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)

        lead = create_lead(
            data["name"],
            data["email"],
            data["phone"],
            data["company"],
            data["status"],
            data["source"]
        )

        lead["_id"] = str(lead["_id"])
        lead["created_at"] = lead["created_at"].isoformat()
        lead["updated_at"] = lead["updated_at"].isoformat()

        return JsonResponse(lead, status=201)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


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