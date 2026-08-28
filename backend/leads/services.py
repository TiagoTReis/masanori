from datetime import datetime, timezone

from bson import ObjectId

from .mongodb import db


def create_lead(name, email, phone, company, status, source):
    lead = {
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "status": status,
        "source": source,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = db.leads.insert_one(lead)

    lead["_id"] = result.inserted_id

    return lead


def get_leads():
    return list(db.leads.find())


def get_lead_by_id(lead_id):
    return db.leads.find_one({"_id": ObjectId(lead_id)})