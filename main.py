from structocr_client import extract_passport
from mrz_parser import parse_passport
from mrz_validation import validate_passport
from viz_parser import parse_viz
from mrz_viz_comparison import compare_mrz_viz


IMAGE_PATH = r"C:\Users\pARTH\Desktop\slovek.jpg"


def main():
    print("========== MRZ PIPELINE ==========")

    raw_data = extract_passport(IMAGE_PATH)
    data = parse_passport(raw_data)
    result = validate_passport(data)

    print("\n========== RESULT ==========")
    print("STATUS:", "VALID" if result["valid"] else "INVALID")

    for key, value in data.items():
        print(f"{key}: {value}")

    if result["errors"]:
        print("\nERRORS:")
        for error in result["errors"]:
            print("-", error)


    viz_result = parse_viz(raw_data)

    if viz_result["status"] == "success":
        viz = viz_result["data"]

        comparison = compare_mrz_viz(data, viz)

        print("\n========== MRZ ↔ VIZ ==========")
        print("STATUS:", comparison["status"])

        for field, check in comparison["checks"].items():
                print(f"{field}: {'MATCH' if check['match'] else 'MISMATCH'}")

        if comparison["mismatches"]:
                print("\nMISMATCHES:")
                for field in comparison["mismatches"]:
                    print("-", field)

    else:
        print("\nVIZ PARSE FAILED")

if __name__ == "__main__":
    main()