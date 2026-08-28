import re


ALLOWED_STATUSES = {
    "new",
    "contacted",
    "qualified",
}

ALLOWED_SOURCES = {
    "website",
    "instagram",
    "linkedin",
}

REQUIRED_FIELDS = {
    "name",
    "email",
    "phone",
    "company",
    "status",
    "source",
}

ALLOWED_FIELDS = REQUIRED_FIELDS


def validate_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def validate_lead(data, partial=False):
    errors = {}

    if not partial:
        missing_fields = REQUIRED_FIELDS - data.keys()

        if missing_fields:
            errors["missing_fields"] = sorted(missing_fields)

    invalid_fields = set(data.keys()) - ALLOWED_FIELDS

    if invalid_fields:
        errors["invalid_fields"] = sorted(invalid_fields)

    if "name" in data and not isinstance(data["name"], str):
        errors["name"] = "Must be a string."

    if "email" in data:
        if not isinstance(data["email"], str):
            errors["email"] = "Must be a string."
        elif not validate_email(data["email"]):
            errors["email"] = "Invalid email."

    if "phone" in data and not isinstance(data["phone"], str):
        errors["phone"] = "Must be a string."

    if "company" in data and not isinstance(data["company"], str):
        errors["company"] = "Must be a string."

    if "status" in data and data["status"] not in ALLOWED_STATUSES:
        errors["status"] = "Invalid status."

    if "source" in data and data["source"] not in ALLOWED_SOURCES:
        errors["source"] = "Invalid source."

    return errors