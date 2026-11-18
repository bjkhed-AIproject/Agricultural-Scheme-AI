
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="Agricultural Scheme AI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agricultural Government Schemes AI")

st.write(
    "Upload agricultural scheme PDFs, fetch information "
    "from the TNAU website, and ask questions using AI."
)

st.divider()


# 1. PDF Upload Section
st.header("1. Upload Agricultural Scheme PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if st.button("Upload PDF", disabled=uploaded_file is None):

    with st.spinner("Uploading and processing PDF..."):

        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{API_URL}/upload-pdf",
                files=files,
                timeout=300
            )

            if response.status_code == 200:
                st.success(
                    "PDF uploaded and processed successfully!"
                )
                st.json(response.json())

            else:
                st.error(f"Upload failed: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend: {e}")


st.divider()


# 2. TNAU Website Section
st.header("2. Update TNAU Website Information")

st.write(
    "Fetch the latest available agricultural schemes "
    "information from the official TNAU website and "
    "store it in the FAISS database."
)

if st.button("Fetch TNAU Website Information"):

    with st.spinner("Fetching TNAU website and updating FAISS..."):

        try:
            response = requests.post(
                f"{API_URL}/ingest-tnau",
                timeout=300
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "TNAU website information updated successfully!"
                )

                st.write(
                    "New chunks added:",
                    result.get("chunks_added", 0)
                )

            else:
                st.error(
                    f"TNAU update failed: {response.text}"
                )

        except requests.exceptions.RequestException as e:
            st.error(
                f"Could not connect to backend: {e}"
            )


st.divider()


# 3. Question and Answer Section
st.header("3. Ask Questions About Agricultural Schemes")

question = st.text_input(
    "Enter your question",
    placeholder=(
        "Example: What subsidy is offered under "
        "the Agricultural Mechanisation Programme?"
    )
)

if st.button("Get Answer", disabled=not question.strip()):

    with st.spinner(
        "Searching documents and generating answer..."
    ):

        try:
            response = requests.post(
                f"{API_URL}/ask",
                params={"question": question},
                timeout=300
            )

            if response.status_code == 200:

                result = response.json()
                answer = result.get("answer", "")

                if isinstance(answer, list):
                    answer = "\n".join(
                        item.get("text", "")
                        for item in answer
                        if isinstance(item, dict)
                    )

                st.subheader("Answer")
                st.write(answer)

            else:
                st.error(f"Error: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(
                f"Could not connect to backend: {e}"
            )


st.divider()

st.caption(
    "Powered by Streamlit, FastAPI, FAISS, "
    "HuggingFace Embeddings and Google Gemini."
)
