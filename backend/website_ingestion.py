
import requests
from bs4 import BeautifulSoup
import os

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


TNAU_URLS = [
    "https://agritech.tnau.ac.in/agricultural_engineering/"
    "agriengg_govt_schemes.html",

    "https://agritech.tnau.ac.in/agricultural_engineering/"
    "agriengg_schemes.html",
]


def fetch_tnau_websites():

    documents = []

    for url in TNAU_URLS:

        print(f"Connecting to: {url}")

        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup([
            "script",
            "style",
            "nav",
            "footer"
        ]):
            element.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        if not text:
            print(f"No text extracted from {url}")
            continue

        print(
            f"Extracted {len(text)} characters "
            f"from {url}"
        )

        document = Document(
            page_content=text,
            metadata={
                "source": "TNAU Government Schemes Website",
                "source_url": url
            }
        )

        documents.append(document)

    if not documents:
        raise ValueError(
            "No information could be extracted from TNAU."
        )

    return documents


def process_tnau_website():

    print("Starting TNAU website ingestion...")

    documents = fetch_tnau_websites()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} website chunks.")

    if not chunks:
        raise ValueError("No text chunks were created.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if not os.path.exists("faiss_db/index.faiss"):
        raise FileNotFoundError(
            "FAISS database not found. Upload a PDF first."
        )

    vector_db = FAISS.load_local(
        "faiss_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Remove previously indexed TNAU website information.
    # Uploaded PDF information will remain untouched.
    existing_ids = [
        doc_id
        for doc_id, doc in vector_db.docstore._dict.items()
        if doc.metadata.get("source")
        == "TNAU Government Schemes Website"
    ]

    if existing_ids:

        print(
            f"Removing {len(existing_ids)} old TNAU chunks..."
        )

        vector_db.delete(ids=existing_ids)

    # Add the latest information from both official pages.
    vector_db.add_documents(chunks)

    vector_db.save_local("faiss_db")

    print("TNAU website information updated successfully!")

    return len(chunks)
