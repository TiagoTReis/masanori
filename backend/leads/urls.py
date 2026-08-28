from django.urls import path

from .views import get_lead, list_leads


urlpatterns = [
    path("leads/", list_leads, name="leads"),
    path("leads/<str:lead_id>/", get_lead, name="get-lead"),
]