
import json
import shutil
import os

from fastapi import FastAPI, UploadFile, File, HTTPException

from backend.ingestion import process_pdf
from backend.retrieval import generate_answer_with_sources
from backend.website_ingestion import process_tnau_website


app = FastAPI(title="Agricultural Scheme AI API")


# Home Endpoint
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
        answer, sources = generate_answer_with_sources(question)

        return {
            "question": question,
            "answer": answer,
            "sources": sources
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


# Scheme Explorer API
@app.get("/schemes")
def get_schemes():

    catalogue_path = "data/schemes.json"

    if not os.path.exists(catalogue_path):
        raise HTTPException(
            status_code=404,
            detail="Scheme catalogue not found"
        )

    try:
        with open(
            catalogue_path,
            "r",
            encoding="utf-8"
        ) as file:
            schemes = json.load(file)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Scheme catalogue contains invalid JSON"
        )

    return {
        "total_schemes": len(schemes),
        "schemes": schemes
    }
