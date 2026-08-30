from datetime import datetime, timezone

from bson import ObjectId

from .mongodb import db


def create_lead(name, email, phone, company, status, source):
    now = datetime.now(timezone.utc)

    lead = {
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "status": status,
        "source": source,
        "created_at": now,
        "updated_at": now,
        "interactions": [
            {
                "type": "created",
                "description": "Lead cadastrado no CRM",
                "created_at": now,
            }
        ],
    }

    result = db.leads.insert_one(lead)

    lead["_id"] = result.inserted_id

    return lead


def get_leads():
    return list(db.leads.find())


def get_lead_by_id(lead_id):
    return db.leads.find_one({"_id": ObjectId(lead_id)})


def update_lead(lead_id, updates):
    updates["updated_at"] = datetime.now(timezone.utc)

    result = db.leads.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": updates}
    )

    if result.matched_count == 0:
        return None

    return get_lead_by_id(lead_id)


def delete_lead(lead_id):
    result = db.leads.delete_one(
        {"_id": ObjectId(lead_id)}
    )

    return result.deleted_count > 0

def add_interaction(lead_id, interaction_type, description):
    interaction = {
        "type": interaction_type,
        "description": description,
        "created_at": datetime.now(timezone.utc),
    }

    result = db.leads.update_one(
        {"_id": ObjectId(lead_id)},
        {"$push": {"interactions": interaction}}
    )

    if result.matched_count == 0:
        return None

    return get_lead_by_id(lead_id)