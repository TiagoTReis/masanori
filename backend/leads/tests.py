import json

from django.test import TestCase, RequestFactory

from .services import (
    create_lead,
    get_leads,
    get_lead_by_id,
    update_lead,
    delete_lead,
)
from .views import list_leads, get_lead


class LeadServiceTestCase(TestCase):

    def test_create_lead(self):
        lead = create_lead(
            "Teste Automatizado",
            "teste@teste.com",
            "12900000000",
            "Empresa Teste",
            "new",
            "test"
        )

        self.assertIsNotNone(lead["_id"])
        self.assertEqual(lead["name"], "Teste Automatizado")
        self.assertEqual(lead["email"], "teste@teste.com")

        delete_lead(str(lead["_id"]))

    def test_get_lead_by_id(self):
        lead = create_lead(
            "Busca Teste",
            "busca@teste.com",
            "12911111111",
            "Empresa Busca",
            "new",
            "test"
        )

        found_lead = get_lead_by_id(str(lead["_id"]))

        self.assertIsNotNone(found_lead)
        self.assertEqual(found_lead["name"], "Busca Teste")
        self.assertEqual(found_lead["email"], "busca@teste.com")

        delete_lead(str(lead["_id"]))

    def test_get_lead_not_found(self):
        lead = get_lead_by_id(
            "000000000000000000000000"
        )

        self.assertIsNone(lead)

    def test_update_lead(self):
        lead = create_lead(
            "Atualização Teste",
            "update@teste.com",
            "12922222222",
            "Empresa Update",
            "new",
            "test"
        )

        updated_lead = update_lead(
            str(lead["_id"]),
            {
                "status": "qualified",
                "phone": "12933333333"
            }
        )

        self.assertIsNotNone(updated_lead)
        self.assertEqual(updated_lead["status"], "qualified")
        self.assertEqual(updated_lead["phone"], "12933333333")
        self.assertIsNotNone(updated_lead["updated_at"])

        delete_lead(str(lead["_id"]))

    def test_update_lead_not_found(self):
        updated_lead = update_lead(
            "000000000000000000000000",
            {
                "status": "qualified"
            }
        )

        self.assertIsNone(updated_lead)

    def test_delete_lead(self):
        lead = create_lead(
            "Delete Teste",
            "delete@teste.com",
            "12944444444",
            "Empresa Delete",
            "new",
            "test"
        )

        deleted = delete_lead(str(lead["_id"]))

        self.assertTrue(deleted)

        found_lead = get_lead_by_id(
            str(lead["_id"])
        )

        self.assertIsNone(found_lead)

    def test_delete_lead_not_found(self):
        deleted = delete_lead(
            "000000000000000000000000"
        )

        self.assertFalse(deleted)


class LeadViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_list_leads_get(self):
        lead = create_lead(
            "Lista Teste",
            "lista@teste.com",
            "12955555555",
            "Empresa Lista",
            "new",
            "test"
        )

        request = self.factory.get("/api/leads/")
        response = list_leads(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Lista Teste",
            response.content
        )

        delete_lead(str(lead["_id"]))

    def test_list_leads_post(self):
        data = {
            "name": "POST Teste",
            "email": "post@teste.com",
            "phone": "12966666666",
            "company": "Empresa POST",
            "status": "new",
            "source": "test"
        }

        request = self.factory.post(
            "/api/leads/",
            data=json.dumps(data),
            content_type="application/json"
        )

        response = list_leads(request)

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            b"POST Teste",
            response.content
        )

        created_lead = get_leads()[-1]

        delete_lead(str(created_lead["_id"]))

    def test_get_lead_view(self):
        lead = create_lead(
            "View Teste",
            "view@teste.com",
            "12977777777",
            "Empresa View",
            "new",
            "test"
        )

        request = self.factory.get(
            f"/api/leads/{lead['_id']}/"
        )

        response = get_lead(
            request,
            str(lead["_id"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"View Teste",
            response.content
        )

        delete_lead(str(lead["_id"]))

    def test_delete_lead_view(self):
        lead = create_lead(
            "Delete View Teste",
            "deleteview@teste.com",
            "12988888888",
            "Empresa Delete View",
            "new",
            "test"
        )

        request = self.factory.delete(
            f"/api/leads/{lead['_id']}/"
        )

        response = get_lead(
            request,
            str(lead["_id"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Lead deleted successfully",
            response.content
        )

        found_lead = get_lead_by_id(
            str(lead["_id"])
        )

        self.assertIsNone(found_lead)