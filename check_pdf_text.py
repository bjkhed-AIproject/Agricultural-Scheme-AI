
import fitz
import pytesseract
from PIL import Image
from io import BytesIO

print("Starting PDF text extraction...")

pdf_path = "documents/Agri pdf.pdf"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_document = fitz.open(pdf_path)

print(f"Total pages: {len(pdf_document)}")

for page_number, page in enumerate(pdf_document):

    print("\n")
    print("=" * 60)
    print(f"PAGE {page_number + 1}")
    print("=" * 60)

    text = page.get_text().strip()

    if not text:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image = Image.open(BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(image, lang="eng").strip()

    print(text)

pdf_document.close()

print("\nPDF extraction finished!")
