
import os
import re
import time

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

_embeddings = None
_vector_db = None

# Minimum relevance score for keeping a retrieved passage.
# Higher scores indicate a more relevant match.
RELEVANCE_THRESHOLD = 0.48

# Maximum number of source passages to return.
MAX_SOURCES = 4


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


def retrieve_relevant_documents(question):
    print("\nSearching for relevant passages...")

    vector_db = load_faiss_database()

    # Retrieve more candidates so we can filter them.
    results = vector_db.similarity_search_with_relevance_scores(
        question,
        k=8
    )

    relevant_documents = []
    seen_content = set()

    for document, score in results:

        print(f"Retrieved relevance score: {score:.3f}")

        # Filter passages below the relevance threshold.
        if score < RELEVANCE_THRESHOLD:
            continue

        # Normalize text to identify duplicate passages.
        normalized_content = re.sub(
            r"\s+",
            " ",
            document.page_content
        ).strip().lower()

        if not normalized_content:
            continue

        if normalized_content in seen_content:
            continue

        seen_content.add(normalized_content)

        relevant_documents.append({
            "document": document,
            "score": float(score)
        })

        if len(relevant_documents) >= MAX_SOURCES:
            break

    print(
        f"Selected {len(relevant_documents)} relevant passages."
    )

    return relevant_documents


def get_retrieved_sources(question):
    results = retrieve_relevant_documents(question)

    sources = []

    for item in results:

        document = item["document"]

        sources.append({
            "content": document.page_content,
            "source": document.metadata.get(
                "source",
                "Unknown source"
            ),
            "source_url": document.metadata.get(
                "source_url",
                ""
            ),
            "relevance_score": round(item["score"], 3)
        })

    return sources


def generate_answer_with_sources(question):
    print("\nSTEP 1: Retrieving relevant documents...")

    start_time = time.time()

    results = retrieve_relevant_documents(question)

    print(
        f"STEP 2: Retrieval completed in "
        f"{time.time() - start_time:.2f} seconds"
    )

    # Prepare source information from the same retrieved passages.
    sources = []

    for item in results:

        document = item["document"]

        sources.append({
            "content": document.page_content,
            "source": document.metadata.get(
                "source",
                "Unknown source"
            ),
            "source_url": document.metadata.get(
                "source_url",
                ""
            ),
            "relevance_score": round(item["score"], 3)
        })

    # If no relevant information was found, do not invent an answer.
    if not results:
        answer = (
            "I could not find sufficiently relevant information "
            "in the uploaded documents or TNAU website data "
            "to answer this question."
        )

        return answer, sources

    # Build context using only the selected relevant passages.
    context = "\n\n".join(
        item["document"].page_content
        for item in results
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

        Instructions:
        1. Give a clear and direct answer.
        2. Use bullet points when explaining multiple benefits.
        3. Do not include information that is not in the context.
        4. If the answer is not available in the context,
           clearly say that the information is not available
           in the provided documents or TNAU website data.
        5. Do not guess subsidy amounts, eligibility conditions,
           or scheme benefits.

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

    response = chain.invoke({
        "context": context,
        "question": question
    })

    print(
        f"STEP 5: Gemini response received in "
        f"{time.time() - gemini_start:.2f} seconds!"
    )

    return response.content, sources


# Backward-compatible function
def generate_answer(question):
    answer, sources = generate_answer_with_sources(question)
    return answer
