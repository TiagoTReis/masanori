from datetime import datetime, timezone

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