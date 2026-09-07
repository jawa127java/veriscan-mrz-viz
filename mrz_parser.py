# import re


# def normalize_mrz_line(line):

#     return "".join(
#         char
#         for char in line.upper()
#         if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"
#     )


# def parse_mrz(raw_mrz):

#     try:

#         # =========================
#         # NORMALIZE OCR LINES
#         # =========================

#         lines = [
#             normalize_mrz_line(line)
#             for line in raw_mrz.splitlines()
#             if line.strip()
#         ]

#         # =========================
#         # FIND MRZ LINES
#         # =========================

#         mrz_lines = [
#             line
#             for line in lines
#             if len(line) == 44
#         ]

#         # Need exactly / at least two valid lines
#         if len(mrz_lines) < 2:

#             return {
#                 "status": "error",
#                 "error": {
#                     "code": "MRZ_PARSE_FAILED",
#                     "message": "Could not identify two valid 44-character MRZ lines"
#                 },
#                 "errors": [],
#                 "evidence": []
#             }

#         # Take last two MRZ candidates
#         line1 = mrz_lines[-2]
#         line2 = mrz_lines[-1]

#         # =========================
#         # BASIC CHARACTER CHECK
#         # =========================

#         if not re.fullmatch(r"[A-Z0-9<]{44}", line1):

#             return {
#                 "status": "error",
#                 "error": {
#                     "code": "MRZ_PARSE_FAILED",
#                     "message": "Invalid characters in MRZ line 1"
#                 },
#                 "errors": [],
#                 "evidence": []
#             }

#         if not re.fullmatch(r"[A-Z0-9<]{44}", line2):

#             return {
#                 "status": "error",
#                 "error": {
#                     "code": "MRZ_PARSE_FAILED",
#                     "message": "Invalid characters in MRZ line 2"
#                 },
#                 "errors": [],
#                 "evidence": []
#             }

#         # =========================
#         # LINE 1
#         # =========================

#         document_type = line1[0]

#         issuing_country = line1[2:5]

#         name_part = line1[5:]

#         name_parts = name_part.split("<<", 1)

#         surname = name_parts[0].replace("<", " ").strip()

#         given_names = []

#         if len(name_parts) > 1:

#             given_names = [
#                 name.replace("<", " ").strip()
#                 for name in name_parts[1].split("<")
#                 if name.strip()
#             ]

#         # =========================
#         # LINE 2
#         # =========================

#         passport_number_raw = line2[0:9]

#         passport_number = passport_number_raw.replace("<", "")

#         passport_number_check = line2[9]

#         nationality = line2[10:13]

#         date_of_birth = line2[13:19]

#         date_of_birth_check = line2[19]

#         sex = line2[20]

#         expiry_date = line2[21:27]

#         expiry_date_check = line2[27]

#         optional_data = line2[28:42]

#         final_check_digit = line2[43]

#         # =========================
#         # RESULT
#         # =========================

#         return {

#             "status": "success",

#             "data": {

#                 "line1": line1,
#                 "line2": line2,

#                 "document_type": document_type,

#                 "issuing_country": issuing_country,

#                 "surname": surname,

#                 "given_names": given_names,

#                 "passport_number": passport_number,

#                 "passport_number_raw": passport_number_raw,

#                 "nationality": nationality,

#                 "date_of_birth": date_of_birth,

#                 "sex": sex,

#                 "expiry_date": expiry_date,

#                 "optional_data": optional_data,

#                 "check_digits": {

#                     "passport_number": passport_number_check,

#                     "date_of_birth": date_of_birth_check,

#                     "expiry_date": expiry_date_check,

#                     "final": final_check_digit
#                 }
#             },

#             "errors": [],

#             "evidence": []
#         }

#     except Exception as e:

#         return {

#             "status": "error",

#             "error": {

#                 "code": "MRZ_PARSE_FAILED",

#                 "message": str(e)
#             },

#             "errors": [],

#             "evidence": []
#         }

def parse_passport(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid StructOCR response")

    return {
        "document_type": data.get("type"),
        "country_code": data.get("country_code"),
        "nationality": data.get("nationality"),
        "passport_number": data.get("passport_number"),
        "surname": data.get("surname"),
        "given_names": data.get("given_names"),
        "sex": data.get("sex"),
        "date_of_birth": data.get("date_of_birth"),
        "place_of_birth": data.get("place_of_birth"),
        "date_of_issue": data.get("date_of_issue"),
        "date_of_expiry": data.get("date_of_expiry"),
        "place_of_issue": data.get("place_of_issue"),
    }