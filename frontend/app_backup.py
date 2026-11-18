
import os
import re
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8001")

TNAU_URL = (
    "https://agritech.tnau.ac.in/agricultural_engineering/"
    "agriengg_govt_schemes.html"
)

st.set_page_config(
    page_title="Tamil Nadu Agricultural Scheme AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# WEBSITE DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #10251b;
    color: #e8f1e9;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

[data-testid="stSidebar"] {
    background-color: #183829;
}

[data-testid="stSidebar"] * {
    color: #e8f1e9;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #b7e4c7;
}

.subtitle {
    font-size: 16px;
    color: #c0d5c5;
    margin-bottom: 20px;
}

.stApp p, .stApp li, .stApp label {
    color: #e1ece3;
}

div.stButton > button {
    background-color: #287747;
    color: white;
    border: 1px solid #4b9b68;
    border-radius: 9px;
    padding: 10px 16px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #35945a;
    color: white;
}

[data-testid="stChatMessage"] {
    background-color: #1b3829;
    border: 1px solid #355b43;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="stChatInput"] {
    background-color: #1b3829;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

[data-testid="stExpander"] {
    background-color: #1b3829;
    border: 1px solid #41664c;
    border-radius: 10px;
}

.stApp a {
    color: #8fd3a7 !important;
}

.scheme-card {
    background-color: #1b3829;
    border: 1px solid #41664c;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}

.scheme-title {
    color: #b7e4c7;
    font-size: 19px;
    font-weight: 700;
}

.source-card {
    background-color: #203d2d;
    border: 1px solid #42694e;
    border-radius: 10px;
    padding: 14px;
    margin-top: 10px;
}

hr {
    border-color: #3c6048;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def clean_source_text(content):

    if not content:
        return ""

    content = re.sub(r"\s+", " ", str(content))

    content = re.sub(
        r"\bTop\b",
        "",
        content,
        flags=re.IGNORECASE
    )

    return content.strip()


def display_sources(sources):

    if not sources:
        st.info("No source information was returned.")
        return

    with st.expander("📚 View Sources Used"):

        for i, source in enumerate(sources, start=1):

            source_name = source.get(
                "source",
                "Unknown source"
            )

            score = source.get("relevance_score")

            content = clean_source_text(
                source.get("content", "")
            )

            st.markdown(f"**📄 Source {i}: {source_name}**")

            if score is not None:
                st.caption(f"Relevance score: {score}")

            if content:
                st.write(content)

            source_url = source.get("source_url", "")

            if source_url:
                st.markdown(
                    f"[Open source document]({source_url})"
                )

            st.divider()


def get_scheme_data():

    try:

        response = requests.get(
            f"{API_URL}/schemes",
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result.get("schemes", [])

    except requests.exceptions.RequestException as e:

        st.error(f"Could not load schemes: {e}")
        return []

    except ValueError:

        st.error("The backend returned invalid scheme data.")
        return []


def display_scheme(scheme):

    name = scheme.get("name") or "Scheme name unavailable"

    number = scheme.get("scheme_number", "")

    st.markdown(
        f'<div class="scheme-title">'
        f'🌾 Scheme {number}: {name}'
        f'</div>',
        unsafe_allow_html=True
    )

    description = scheme.get("description")

    if description:
        st.write(description)

    st.markdown("**💰 Subsidy / Benefits**")

    subsidy = scheme.get("subsidy")

    if subsidy:
        st.write(subsidy)
    else:
        st.info(
            "Specific subsidy details are not available "
            "in the extracted catalogue."
        )

    with st.expander("View full scheme details"):

        fields = [
            ("Project Area", "project_area"),
            ("Eligibility", "eligibility"),
            ("How to Apply", "how_to_apply"),
            ("Required Documents", "required_documents"),
            ("Contact Office", "contact_office")
        ]

        for label, key in fields:

            value = scheme.get(key)

            if value:

                st.markdown(f"**{label}**")

                if isinstance(value, list):
                    for item in value:
                        st.write(f"- {item}")
                else:
                    st.write(value)

        districts = scheme.get("districts") or []

        if districts:
            st.markdown("**Districts**")
            st.write(", ".join(districts))

        source_url = (
            scheme.get("source_url")
            or scheme.get("application_url")
            or TNAU_URL
        )

        st.markdown(
            f"[View official TNAU source]({source_url})"
        )

    st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🌾 Scheme Assistant")

    st.markdown("### Knowledge Sources")

    st.markdown(
        f"[Visit TNAU Official Website]({TNAU_URL})"
    )

    st.divider()

    st.markdown("### 📄 Upload Scheme PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button(
            "Upload and Process PDF",
            use_container_width=True
        ):

            with st.spinner("Processing PDF..."):

                try:

                    response = requests.post(
                        f"{API_URL}/upload-pdf",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=300
                    )

                    if response.status_code == 200:
                        st.success("PDF uploaded successfully!")
                    else:
                        st.error(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed: {e}")

    st.divider()

    st.markdown("### 🌐 TNAU Website Data")

    if st.button(
        "Update TNAU Information",
        use_container_width=True
    ):

        with st.spinner("Updating TNAU information..."):

            try:

                response = requests.post(
                    f"{API_URL}/ingest-tnau",
                    timeout=300
                )

                if response.status_code == 200:
                    st.success("TNAU information updated!")
                else:
                    st.error(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Update failed: {e}")

    st.divider()

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Streamlit • FastAPI • FAISS • Gemini")


# --------------------------------------------------
# MAIN WEBSITE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">'
    '🌾 Tamil Nadu Agricultural Scheme AI'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent assistant for agricultural '
    'government schemes in Tamil Nadu.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# MAIN WEBSITE TABS
# --------------------------------------------------

scheme_tab, chatbot_tab = st.tabs([
    "🌾 Scheme Explorer",
    "💬 AI Chatbot"
])


# --------------------------------------------------
# SCHEME EXPLORER
# --------------------------------------------------

with scheme_tab:

    st.markdown("## 🌾 Explore Government Schemes")

    st.write(
        "Search and explore agricultural schemes offered "
        "by the Tamil Nadu Agricultural Engineering Department."
    )

    schemes = get_scheme_data()

    if schemes:

        st.success(
            f"Successfully loaded {len(schemes)} schemes."
        )

        search_text = st.text_input(
            "🔍 Search schemes",
            placeholder="Search by scheme name, subsidy, crop or keyword..."
        )

        all_districts = sorted({
            district
            for scheme in schemes
            for district in (scheme.get("districts") or [])
        })

        selected_district = st.selectbox(
            "Filter by district",
            ["All Districts"] + all_districts
        )

        filtered_schemes = []

        for scheme in schemes:

            searchable_text = " ".join([
                str(scheme.get("name") or ""),
                str(scheme.get("description") or ""),
                str(scheme.get("subsidy") or ""),
                str(scheme.get("project_area") or ""),
                str(scheme.get("eligibility") or "")
            ]).lower()

            if search_text.lower() not in searchable_text:
                continue

            scheme_districts = scheme.get("districts") or []

            if (
                selected_district != "All Districts"
                and selected_district not in scheme_districts
            ):
                continue

            filtered_schemes.append(scheme)

        st.markdown(
            f"### Showing {len(filtered_schemes)} scheme(s)"
        )

        if filtered_schemes:

            for scheme in filtered_schemes:

                with st.container():

                    st.markdown(
                        '<div class="scheme-card">',
                        unsafe_allow_html=True
                    )

                    display_scheme(scheme)

                    st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.warning(
                "No schemes match your search. "
                "Try another keyword or district."
            )

        st.caption(
            "Scheme information is extracted from the TNAU source. "
            "Please confirm current eligibility and subsidy details "
            "with the relevant Agricultural Engineering Department "
            "office before applying."
        )

    else:

        st.warning(
            "Scheme catalogue could not be loaded. "
            "Please check that the FastAPI backend is running."
        )


# --------------------------------------------------
# AI CHATBOT
# --------------------------------------------------

with chatbot_tab:

    st.markdown("## 💬 Ask the Agricultural Scheme Assistant")

    st.write(
        "Ask questions about agricultural schemes in "
        "Tamil Nadu. The AI assistant searches the available "
        "documents and provides answers with sources."
    )

    if not st.session_state.messages:

        st.markdown("### 💡 Try asking")

        examples = [
            "What subsidy is offered under the Agricultural Mechanisation Programme?",
            "What benefits are available under Scheme No. 7?",
            "Explain the Soil and Water Conservation Scheme.",
            "What is the Command Area Development Programme?"
        ]

        columns = st.columns(2)

        for i, example in enumerate(examples):

            with columns[i % 2]:

                if st.button(
                    example,
                    key=f"example_{i}",
                    use_container_width=True
                ):

                    st.session_state.pending_question = example
                    st.rerun()

    # Previous conversation

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):
                display_sources(message["sources"])

    pending_question = st.session_state.pop(
        "pending_question",
        None
    )

    question = st.chat_input(
        "Ask anything about Tamil Nadu agricultural schemes..."
    )

    if pending_question:
        question = pending_question

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching documents and generating your answer..."
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

                        sources = result.get("sources", [])

                        st.markdown(answer)

                        display_sources(sources)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })

                    else:

                        error_message = (
                            f"Something went wrong: {response.text}"
                        )

                        st.error(error_message)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_message
                        })

                except requests.exceptions.RequestException as e:

                    error_message = (
                        f"Could not connect to the backend: {e}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Tamil Nadu Agricultural Scheme AI | "
    "Streamlit • FastAPI • FAISS • HuggingFace • Google Gemini"
)
