# 🌾 Agricultural Government Schemes AI

## Project Overview

Agricultural Government Schemes AI is a Retrieval-Augmented Generation (RAG) application that helps users find information about agricultural government schemes.

Users can upload agricultural scheme PDF documents, retrieve information from the official Tamil Nadu Agricultural University (TNAU) website, and ask questions through an AI-powered interface.

## Technologies Used

- Python
- Streamlit – Frontend
- FastAPI – Backend
- FAISS – Vector Database
- HuggingFace Sentence Transformers – Text Embeddings
- Google Gemini – AI Response Generation
- LangChain – RAG Pipeline
- PyMuPDF and Tesseract OCR – PDF Text Extraction
- BeautifulSoup – Website Data Extraction

## Data Sources

1. Uploaded agricultural government scheme PDF documents.
2. Official TNAU Agricultural Engineering Government Schemes website:

   https://agritech.tnau.ac.in/agricultural_engineering/agriengg_govt_schemes.html

## Main Features

- Upload agricultural scheme PDF documents.
- Extract text from scanned PDFs using OCR.
- Fetch agricultural scheme information from the TNAU website.
- Split documents into text chunks.
- Generate embeddings using HuggingFace.
- Store and retrieve information using FAISS.
- Ask questions in natural language.
- Generate answers using Google Gemini.

## Project Structure

```text
Agricultural_Scheme_AI/
│
├── backend/
│   ├── main.py
│   ├── ingestion.py
│   ├── retrieval.py
│   └── website_ingestion.py
│
├── frontend/
│   └── app.py
│
├── documents/
├── faiss_db/
├── venv/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Create and activate a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required libraries:

```powershell
python -m pip install -r requirements.txt
```

Install Tesseract OCR separately on Windows and ensure its executable is available at:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## API Configuration

Create a `.env` file in the project root and add your Google Gemini API key:

```text
GOOGLE_API_KEY=your_google_api_key
```

Do not upload your `.env` file to GitHub.

## Running the Application

### Start the FastAPI backend

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

### Start the Streamlit frontend

Open another terminal and run:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py --server.port 8502
```

Open the application:

http://localhost:8502

FastAPI documentation:

http://127.0.0.1:8001/docs

## RAG Workflow

1. Upload a PDF or fetch information from the TNAU website.
2. Extract and split the source information into text chunks.
3. Convert the chunks into vector embeddings.
4. Store the embeddings in FAISS.
5. Retrieve relevant information when a user asks a question.
6. Send the retrieved context to Google Gemini.
7. Display the generated answer in Streamlit.

## Project Objective

To make agricultural government scheme information easier to access through an AI-powered question-answering system.