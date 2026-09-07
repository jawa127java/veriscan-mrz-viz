import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException

from structocr_client import extract_passport
from mrz_parser import parse_passport
from mrz_validation import validate_passport
from viz_parser import parse_viz
from mrz_viz_comparison import compare_mrz_viz

app = FastAPI(title="Passport OCR Pipeline API")

@app.post("/process-passport")
async def process_passport(file: UploadFile = File(...)):
    temp_file_path = None
    try:
        suffix = os.path.splitext(file.filename)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        raw_data = extract_passport(temp_file_path)
        mrz_data = parse_passport(raw_data)
        validation_result = validate_passport(mrz_data)
        viz_result = parse_viz(raw_data)

        response = {
            "mrz_data": mrz_data,
            "mrz_valid": validation_result.get("valid", False),
            "errors": validation_result.get("errors", []),
            "viz_status": viz_result.get("status"),
            "comparison": None
        }

        if viz_result.get("status") == "success":
            viz_data = viz_result["data"]
            comparison = compare_mrz_viz(mrz_data, viz_data)
            response["comparison"] = comparison

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
