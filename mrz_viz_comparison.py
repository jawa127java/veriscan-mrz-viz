from datetime import date


def normalize_text(value):
    return str(value or "").strip().upper()


def normalize_date(value):
    try:
        return date.fromisoformat(str(value).strip()).isoformat()
    except (ValueError, TypeError):
        return None


def compare_mrz_viz(mrz, viz):
    checks = {}
    mismatches = []

    text_fields = {
        "passport_number": ("passport_number", "passport_number"),
        "surname": ("surname", "surname"),
        "given_names": ("given_names", "given_names"),
        "nationality": ("nationality", "nationality"),
        "sex": ("sex", "sex"),
    }

    for field, (mrz_field, viz_field) in text_fields.items():
        mrz_value = normalize_text(mrz.get(mrz_field))
        viz_value = normalize_text(viz.get(viz_field))

        match = bool(mrz_value and viz_value and mrz_value == viz_value)

        checks[field] = {
            "mrz": mrz_value,
            "viz": viz_value,
            "match": match
        }

        if not match:
            mismatches.append(field)

    # DATE OF BIRTH
    mrz_dob = normalize_date(mrz.get("date_of_birth"))
    viz_dob = normalize_date(viz.get("date_of_birth"))

    dob_match = bool(mrz_dob and viz_dob and mrz_dob == viz_dob)

    checks["date_of_birth"] = {
        "mrz": mrz_dob,
        "viz": viz_dob,
        "match": dob_match
    }

    if not dob_match:
        mismatches.append("date_of_birth")

    # EXPIRY DATE
    mrz_expiry = normalize_date(mrz.get("date_of_expiry"))
    viz_expiry = normalize_date(viz.get("date_of_expiry"))

    expiry_match = bool(
        mrz_expiry and viz_expiry and mrz_expiry == viz_expiry
    )

    checks["expiry_date"] = {
        "mrz": mrz_expiry,
        "viz": viz_expiry,
        "match": expiry_match
    }

    if not expiry_match:
        mismatches.append("expiry_date")

    return {
        "status": "MATCH" if not mismatches else "MISMATCH",
        "checks": checks,
        "mismatches": mismatches
    }