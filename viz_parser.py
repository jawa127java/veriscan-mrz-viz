# viz_parser.py

def parse_viz(data):
    if not isinstance(data, dict):
        return {
            "status": "error",
            "error": "Invalid VIZ data"
        }

    return {
        "status": "success",
        "data": {
            "passport_number": str(data.get("passport_number", "")).strip(),
            "surname": str(data.get("surname", "")).strip().upper(),
            "given_names": str(data.get("given_names", "")).strip().upper(),
            "nationality": str(data.get("nationality", "")).strip().upper(),
            "sex": str(data.get("sex", "")).strip().upper(),
            "date_of_birth": str(data.get("date_of_birth", "")).strip(),
            "date_of_issue": str(data.get("date_of_issue", "")).strip(),
            "date_of_expiry": str(data.get("date_of_expiry", "")).strip(),
            "place_of_birth": str(data.get("place_of_birth", "")).strip(),
            "place_of_issue": str(data.get("place_of_issue", "")).strip(),
        }
    }