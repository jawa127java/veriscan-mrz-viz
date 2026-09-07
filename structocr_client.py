# import os
# import base64
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("STRUCTOCR_API_KEY")
# IMAGE_PATH = r"C:\Users\pARTH\Desktop\jathin.jpg"

# if not API_KEY:
#     raise RuntimeError("STRUCTOCR_API_KEY not found")

# print("API key loaded:", True)
# print("Reading image...")

# with open(IMAGE_PATH, "rb") as f:
#     image_b64 = base64.b64encode(f.read()).decode("utf-8")

# payload = {
#     "img": f"data:image/jpeg;base64,{image_b64}"
# }

# print("Sending to StructOCR...")

# response = requests.post(
#     "https://api.structocr.com/v1/passport",
#     headers={
#         "Content-Type": "application/json",
#         "x-api-key": API_KEY,
#     },
#     json=payload,
#     timeout=60,
# )

# print("HTTP STATUS:", response.status_code)
# print("RESPONSE:")
# print(response.text)

import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.structocr.com/v1/passport"


def extract_passport(image_path):
    api_key = os.getenv("STRUCTOCR_API_KEY")

    if not api_key:
        raise RuntimeError("STRUCTOCR_API_KEY is not set")

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        json={
            "img": f"data:image/jpeg;base64,{image_b64}"
        },
        timeout=60,
    )

    print("HTTP STATUS:", response.status_code)

    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise RuntimeError(result)

    return result["data"]