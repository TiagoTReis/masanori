from django.urls import path

from .views import list_leads


urlpatterns = [
    path("leads/", list_leads, name="list-leads"),
]