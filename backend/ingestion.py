
import os
import fitz
import pytesseract

from PIL import Image
from io import BytesIO

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def load_and_split_pdf(pdf_path):

    documents = []

    # Open PDF
    pdf_document = fitz.open(pdf_path)

    print("PDF opened successfully!")
    print(f"Total pages: {len(pdf_document)}")

    # Read each page
    for page_number, page in enumerate(pdf_document):

        # First try normal text extraction
        text = page.get_text().strip()

        # If no text, use OCR
        if not text:

            print(f"Using OCR on page {page_number + 1}")

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image = Image.open(
                BytesIO(pix.tobytes("png"))
            )

            text = pytesseract.image_to_string(
                image,
                lang="eng"
            ).strip()

        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": os.path.basename(pdf_path),
                        "page": page_number + 1
                    }
                )
            )

    pdf_document.close()

    print(f"Pages with extracted text: {len(documents)}")

    if not documents:
        raise ValueError(
            "No text could be extracted from this PDF."
        )

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total text chunks: {len(chunks)}")

    if not chunks:
        raise ValueError("No text chunks were generated.")

    return chunks


def create_and_save_faiss(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Add to existing database if one exists
    if os.path.exists("faiss_db/index.faiss"):

        vector_db = FAISS.load_local(
            "faiss_db",
            embeddings,
            allow_dangerous_deserialization=True
        )

        vector_db.add_documents(chunks)

    else:

        vector_db = FAISS.from_documents(
            chunks,
            embeddings
        )

    os.makedirs("faiss_db", exist_ok=True)

    vector_db.save_local("faiss_db")

    print("FAISS database saved successfully!")

    return vector_db


def process_pdf(pdf_path):

    chunks = load_and_split_pdf(pdf_path)

    vector_db = create_and_save_faiss(chunks)

    print("PDF processing completed successfully!")

    return vector_db

