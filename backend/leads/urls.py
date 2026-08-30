from django.urls import path

from .views import (
    get_lead,
    list_leads,
    add_lead_interaction,
)


urlpatterns = [
    path("leads/", list_leads, name="leads"),
    path("leads/<str:lead_id>/", get_lead, name="get-lead"),
    path(
        "leads/<str:lead_id>/interactions/",
        add_lead_interaction,
        name="add-lead-interaction",
    ),
]