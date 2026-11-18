# 🌾 உழவனின் உரிமைக்கரம்
## Tamil Nadu Agricultural Scheme AI Assistant

### Project Overview

உழவனின் உரிமைக்கரம் is a multilingual AI-powered agricultural government scheme assistant developed as part of my Generative AI course.

The application helps farmers discover Tamil Nadu agricultural government schemes, understand scheme benefits and subsidies, and obtain answers to their questions in English and Tamil.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from agricultural scheme documents and the Tamil Nadu Agricultural University (TNAU) website before generating answers using Google Gemini.

### Problem Statement

Farmers may find it difficult to access, understand and navigate information about government agricultural schemes.

This project aims to make agricultural scheme information easier to find and understand through a simple, multilingual AI-powered application.

### Key Features

- **Scheme Explorer:** Browse 15 agricultural government schemes.
- **Search and Filter:** Find schemes using search and district filters.
- **AI Chatbot:** Ask questions about agricultural schemes in natural language.
- **Tamil and English Support:** Select the preferred language.
- **RAG-Based Answers:** Retrieve relevant information before generating answers.
- **Source References:** Display supporting source information with chatbot answers.
- **PDF Ingestion:** Upload agricultural scheme PDF documents.
- **Website Ingestion:** Retrieve information from the official TNAU website.
- **Farmer Training:** Dedicated section for agricultural training programme information.
- **Responsive Interface:** Dark green-themed Streamlit interface.

### Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend application |
| FastAPI | Backend API |
| LangChain | RAG workflow |
| FAISS | Vector database |
| HuggingFace Sentence Transformers | Text embeddings |
| Google Gemini | AI answer generation |
| PyMuPDF / PyPDF | PDF processing |
| Tesseract OCR | Text extraction from scanned PDFs |
| BeautifulSoup | Website content extraction |

### System Architecture

1. **Data Sources:** Agricultural scheme PDFs and the official TNAU website.
2. **Ingestion:** Extract and split documents into text chunks.
3. **Embedding:** Convert text chunks into vector embeddings using HuggingFace.
4. **Vector Storage:** Store and search embeddings using FAISS.
5. **Retrieval:** Retrieve relevant passages for the user's question.
6. **Generation:** Send retrieved context and the question to Google Gemini.
7. **Response:** Display the generated answer and supporting sources through Streamlit.

### Official Data Source

Tamil Nadu Agricultural University (TNAU) – Agricultural Engineering Government Schemes:

https://agritech.tnau.ac.in/agricultural_engineering/agriengg_govt_schemes.html

### Project Structure

```text
Agricultural_Scheme_AI/
│
├── backend/
│   ├── ingestion.py
│   ├── main.py
│   ├── retrieval.py
│   ├── scheme_catalogue.py
│   ├── split_scheme_sections.py
│   └── website_ingestion.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── original_pdf_text.txt
│   ├── schemes.json
│   ├── schemes_raw.json
│   └── scheme_sections.json
│
├── faiss_db/
│   ├── index.faiss
│   └── index.pkl
│
├── documents/       # Local uploaded documents
├── .env             # Private API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

### Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/bjkhed-AIproject/Agricultural-Scheme-AI.git
```

**2. Open the project folder**

```bash
cd Agricultural-Scheme-AI
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment (Windows PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**5. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**6. Configure the Gemini API key**

Create a `.env` file in the project root folder and add:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Keep your API key private. Never upload the `.env` file to GitHub.

### Running the Application

The application uses two separate terminals.

**Terminal 1 – Start FastAPI backend**

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

Backend URL:

http://127.0.0.1:8001

API documentation:

http://127.0.0.1:8001/docs

**Terminal 2 – Start Streamlit frontend**

```powershell
python -m streamlit run frontend/app.py --server.port 8502
```

Frontend URL:

http://localhost:8502

### Expected Outcome

The application provides farmers with an accessible way to explore agricultural schemes, understand available benefits and subsidies, and ask questions using an AI-powered multilingual chatbot.

### Future Enhancements

- Online deployment for wider farmer access.
- More agricultural government scheme databases.
- Improved Tamil-language responses.
- Additional regional language support.
- Integration with more official government information sources.

### Disclaimer

This application is an educational project developed for a Generative AI course. Scheme eligibility, subsidy amounts, application procedures and other official details should be verified with the relevant government department before making decisions.

---

**Developed as part of a Generative AI learning project.**