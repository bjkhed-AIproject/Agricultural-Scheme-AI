
import os
import time

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Load embedding model only once
_embeddings = None
_vector_db = None


def get_embeddings():

    global _embeddings

    if _embeddings is None:
        print("Loading HuggingFace embedding model...")

        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    return _embeddings


def load_faiss_database():

    global _vector_db

    if _vector_db is not None:
        return _vector_db

    if not os.path.exists("faiss_db/index.faiss"):
        raise FileNotFoundError(
            "FAISS database not found. Upload a PDF first."
        )

    print("Loading FAISS database...")

    _vector_db = FAISS.load_local(
        "faiss_db",
        get_embeddings(),
        allow_dangerous_deserialization=True
    )

    print("FAISS database loaded successfully!")

    return _vector_db


def search_documents(question):

    print("Searching documents in FAISS...")

    vector_db = load_faiss_database()

    results = vector_db.similarity_search(
        question,
        k=4
    )

    print(f"Retrieved {len(results)} documents successfully!")

    return results


def generate_answer(question):

    print("\nSTEP 1: Starting document search...")
    start_time = time.time()

    documents = search_documents(question)

    print(
        f"STEP 2: Document search completed in "
        f"{time.time() - start_time:.2f} seconds"
    )

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file."
        )

    print("STEP 3: Connecting to Gemini...")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key,
        temperature=0,
        timeout=60,
        max_retries=1
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an Agricultural Government Schemes Assistant.

        Answer the user's question using only the information
        provided in the context below.

        If the answer is not available in the context,
        clearly say that the information is not available
        in the provided documents or TNAU website data.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )

    chain = prompt | llm

    print("STEP 4: Sending question to Gemini...")
    gemini_start = time.time()

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    print(
        f"STEP 5: Gemini response received in "
        f"{time.time() - gemini_start:.2f} seconds!"
    )

    return response.content
