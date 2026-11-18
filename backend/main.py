
from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.ingestion import process_pdf
from backend.retrieval import generate_answer
from backend.website_ingestion import process_tnau_website

import shutil
import os

app = FastAPI(title="Agricultural Scheme AI API")


@app.get("/")
def home():
    return {
        "message": "Agricultural Scheme AI Backend is running!"
    }


# PDF Upload Endpoint
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs("documents", exist_ok=True)

    file_path = os.path.join("documents", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        process_pdf(file_path)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "message": "PDF uploaded and processed successfully!",
        "filename": file.filename
    }


# TNAU Website Ingestion Endpoint
@app.post("/ingest-tnau")
def ingest_tnau():

    try:
        total_chunks = process_tnau_website()

        return {
            "message": "TNAU website information updated successfully!",
            "chunks_added": total_chunks
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Question and Answer Endpoint
@app.post("/ask")
async def ask_question(question: str):

    try:
        answer = generate_answer(question)

        return {
            "question": question,
            "answer": answer
        }

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

