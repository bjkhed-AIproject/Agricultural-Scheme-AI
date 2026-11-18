
import fitz
import pytesseract
from PIL import Image
from io import BytesIO

pdf_path = "documents/Agri pdf.pdf"
output_path = "data/original_pdf_text.txt"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf = fitz.open(pdf_path)

print("Total PDF pages:", len(pdf))
print("Starting OCR extraction...")

with open(output_path, "w", encoding="utf-8") as file:

    for page_number, page in enumerate(pdf, start=1):

        print(f"Reading page {page_number} of {len(pdf)}...")

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image = Image.open(
            BytesIO(pix.tobytes("png"))
        )

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        file.write(
            f"\n\n===== PAGE {page_number} =====\n\n"
        )

        file.write(text)

print("\nOCR extraction completed!")
print("Saved to:", output_path)
