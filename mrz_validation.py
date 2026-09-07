import re
from datetime import date,datetime


MRZ_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"

def validate_passport(data):
    errors = []

    required = [
        "document_type",
        "country_code",
        "passport_number",
        "surname",
        "given_names",
        "sex",
        "date_of_birth",
        "date_of_issue",
        "date_of_expiry",
    ]

    for field in required:
        if not data.get(field):
            errors.append(f"Missing field: {field}")

    if data.get("document_type") != "passport":
        errors.append("Invalid document type")

    if data.get("country_code"):
        if not re.fullmatch(r"[A-Z]{3}", data["country_code"]):
            errors.append("Invalid country code")

    if data.get("passport_number"):
        if not re.fullmatch(r"[A-Z0-9<]+", data["passport_number"]):
            errors.append("Invalid passport number")

    if data.get("sex") not in ("M", "F", "X", "<"):
        errors.append("Invalid sex")

    for field in ("date_of_birth", "date_of_issue", "date_of_expiry"):
        try:
            date.fromisoformat(data[field])
        except (KeyError, ValueError):
            errors.append(f"Invalid date: {field}")

    return {
        "valid": not errors,
        "errors": errors
    }

def check_digit(value):
    weights = [7, 3, 1]
    total = 0

    for i, char in enumerate(value):
        if char == "<":
            number = 0
        elif char.isdigit():
            number = int(char)
        elif char.isalpha():
            number = ord(char) - ord("A") + 10
        else:
            return None

        total += number * weights[i % 3]

    return str(total % 10)


def valid_date(value):
    if len(value) != 6 or not value.isdigit():
        return False

    try:
        datetime.strptime(value, "%y%m%d")
        return True
    except ValueError:
        return False


def valid_line1(line1):
    if len(line1) != 44:
        return False

    if line1[0] != "P":
        return False

    if line1[1] != "<":
        return False

    if not line1[2:5].isalpha():
        return False

    return all(char in MRZ_CHARS for char in line1)


def valid_line2(line2):
    if len(line2) != 44:
        return False

    if not all(char in MRZ_CHARS for char in line2):
        return False

    # Passport number
    passport_number = line2[0:9]
    passport_check = line2[9]

    if check_digit(passport_number) != passport_check:
        return False

    # Nationality
    nationality = line2[10:13]

    if not nationality.isalpha():
        return False

    # Date of birth
    dob = line2[13:19]
    dob_check = line2[19]

    if not valid_date(dob):
        return False

    if check_digit(dob) != dob_check:
        return False

    # Sex
    sex = line2[20]

    if sex not in "MF<":
        return False

    # Expiry
    expiry = line2[21:27]
    expiry_check = line2[27]

    if not valid_date(expiry):
        return False

    if check_digit(expiry) != expiry_check:
        return False

    # Final composite check
    composite_data = (
        line2[0:10]
        + line2[13:20]
        + line2[21:43]
    )

    if check_digit(composite_data) != line2[43]:
        return False

    return True


def validate_mrz(line1, line2):
    errors = []

    if not valid_line1(line1):
        errors.append("Invalid MRZ line 1")

    if not valid_line2(line2):
        errors.append("Invalid MRZ line 2")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }