import cv2
import pytesseract


def extract_viz(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Mild preprocessing
    gray = cv2.resize(gray, None, fx=2, fy=2)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Mild contrast enhancement
    gray = cv2.equalizeHist(gray)

    text = pytesseract.image_to_string(
        gray,
        config="--oem 3 --psm 6"
    )

    return text


image_path = r""

text = extract_viz(image_path)

print("========== VIZ OCR ==========")
print(text)