
import os
import re
import requests
import streamlit as st

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_URL = os.getenv("API_URL", "http://127.0.0.1:8001")

TNAU_URL = (
    "https://agritech.tnau.ac.in/"
    "agricultural_engineering/agriengg_govt_schemes.html"
)

st.set_page_config(
    page_title="உழவனின் உரிமைக்கரம் | Agricultural Scheme AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# LANGUAGE TEXT
# --------------------------------------------------

TEXT = {
    "English": {
        "explorer": "🌱 Scheme Explorer",
        "chatbot": "💬 AI Chatbot",
        "training": "🎓 Training Programmes",
        "explore_heading": "🌱 Explore Agricultural Schemes",
        "explore_description": (
            "Search government agricultural schemes and explore "
            "their benefits, eligibility and application details."
        ),
        "search": "🔍 Search schemes",
        "search_placeholder": "Search by scheme name, subsidy, crop or benefit...",
        "district": "📍 Filter by District",
        "all_districts": "All Districts",
        "chat_heading": "💬 Ask the Agricultural Scheme AI",
        "chat_description": (
            "Ask questions about agricultural schemes, subsidies, "
            "eligibility and application procedures."
        ),
        "try_asking": "Try asking:",
        "chat_placeholder": "Type your agricultural scheme question here...",
        "about": "About this scheme",
        "subsidy": "Subsidy / Benefits",
        "eligibility": "Eligibility",
        "project_area": "Project Area",
        "application": "How to Apply",
        "sources": "📚 Information Sources",
        "no_schemes": "No schemes found. Try another search term or district.",
        "showing": "Showing",
        "of": "of",
        "schemes": "schemes",
        "important": "Important:",
        "disclaimer": (
            "Scheme information is provided for general guidance. "
            "Subsidy amounts, eligibility, availability and application "
            "procedures may change. Please confirm the latest details "
            "with the relevant Agriculture Department or "
            "Agricultural Engineering office."
        ),
        "assistant": "Agricultural Scheme AI Assistant",
        "available": "Available Schemes",
        "information": "Information Support",
        "knowledge": "Knowledge Sources",
        "powered": "Built with FastAPI • Streamlit • Retrieval-Augmented Generation",
        "pdf": "📄 Upload Scheme PDF",
        "upload": "Upload PDF",
        "upload_success": "PDF uploaded successfully!",
        "tnau": "🌐 TNAU Website Data",
        "update": "Update TNAU Data",
        "update_success": "TNAU data update completed!",
        "clear": "🗑️ Clear Chat",
        "language": "🌐 Select Language / மொழியைத் தேர்ந்தெடுக்கவும்",
        "answer_language": "Please answer in English.",
        "examples": [
            "What subsidy is offered under the Agricultural Mechanisation Programme?",
            "Who is eligible for agricultural machinery subsidies?",
            "How can farmers apply for government agricultural schemes?",
        ],
        "example_label": "💡 Example",
        "training_heading": "🎓 Farmer Training Programmes",
        "training_description": (
            "Explore the farmer training information available "
            "in the current agricultural scheme data."
        ),
        "training_contact": (
            "For current training dates, venues and registration details, "
            "contact your nearest Agricultural Engineering Department office."
        ),
        "no_training": (
            "No dedicated training programme information was found "
            "in the current scheme data."
        ),
    },

    "தமிழ்": {
        "explorer": "🌱 திட்டங்களை ஆராயுங்கள்",
        "chatbot": "💬 AI உதவியாளர்",
        "training": "🎓 விவசாயிகள் பயிற்சி",
        "explore_heading": "🌱 வேளாண் திட்டங்களை ஆராயுங்கள்",
        "explore_description": (
            "அரசு வேளாண் திட்டங்கள், மானியங்கள், "
            "தகுதிகள் மற்றும் விண்ணப்ப விவரங்களைத் தேடுங்கள்."
        ),
        "search": "🔍 திட்டங்களைத் தேடுங்கள்",
        "search_placeholder": "திட்டம், மானியம் அல்லது பயன் அடிப்படையில் தேடுங்கள்...",
        "district": "📍 மாவட்டத்தைத் தேர்ந்தெடுக்கவும்",
        "all_districts": "அனைத்து மாவட்டங்களும்",
        "chat_heading": "💬 வேளாண் திட்டங்கள் குறித்து கேளுங்கள்",
        "chat_description": (
            "வேளாண் திட்டங்கள், மானியங்கள், தகுதிகள் "
            "மற்றும் விண்ணப்ப முறைகள் பற்றி கேளுங்கள்."
        ),
        "try_asking": "இந்தக் கேள்விகளைக் கேட்கலாம்:",
        "chat_placeholder": "உங்கள் கேள்வியை இங்கே உள்ளிடவும்...",
        "about": "திட்டத்தைப் பற்றிய விவரம்",
        "subsidy": "மானியம் / நன்மைகள்",
        "eligibility": "தகுதிகள்",
        "project_area": "திட்டப் பகுதி",
        "application": "விண்ணப்பிக்கும் முறை",
        "sources": "📚 தகவல் ஆதாரங்கள்",
        "no_schemes": "திட்டங்கள் எதுவும் கிடைக்கவில்லை. வேறு சொல்லைப் பயன்படுத்தித் தேடுங்கள்.",
        "showing": "காண்பிக்கப்படுவது",
        "of": "மொத்தம்",
        "schemes": "திட்டங்கள்",
        "important": "முக்கிய குறிப்பு:",
        "disclaimer": (
            "இந்தத் தகவல்கள் பொதுவான வழிகாட்டுதலுக்காக வழங்கப்படுகின்றன. "
            "மானியம், தகுதி மற்றும் விண்ணப்ப நடைமுறைகள் மாறக்கூடும். "
            "சமீபத்திய விவரங்களுக்கு சம்பந்தப்பட்ட வேளாண்மைத் துறை "
            "அல்லது வேளாண் பொறியியல் அலுவலகத்தை அணுகவும்."
        ),
        "assistant": "வேளாண் திட்ட AI உதவியாளர்",
        "available": "கிடைக்கும் திட்டங்கள்",
        "information": "தகவல் உதவி",
        "knowledge": "தகவல் ஆதாரங்கள்",
        "powered": "FastAPI • Streamlit • Retrieval-Augmented Generation",
        "pdf": "📄 திட்ட PDF பதிவேற்றம்",
        "upload": "PDF பதிவேற்றவும்",
        "upload_success": "PDF வெற்றிகரமாக பதிவேற்றப்பட்டது!",
        "tnau": "🌐 TNAU இணையதளத் தகவல்கள்",
        "update": "TNAU தகவல்களைப் புதுப்பிக்கவும்",
        "update_success": "TNAU தகவல்கள் புதுப்பிக்கப்பட்டன!",
        "clear": "🗑️ உரையாடலை அழிக்கவும்",
        "language": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "answer_language": "Please answer in Tamil.",
        "examples": [
            "வேளாண் இயந்திரமயமாக்கல் திட்டத்தில் எவ்வளவு மானியம் வழங்கப்படுகிறது?",
            "வேளாண் இயந்திர மானியம் பெற யார் தகுதியுடையவர்கள்?",
            "அரசு வேளாண் திட்டங்களுக்கு விவசாயிகள் எவ்வாறு விண்ணப்பிப்பது?",
        ],
        "example_label": "💡 எடுத்துக்காட்டு",
        "training_heading": "🎓 விவசாயிகளுக்கான பயிற்சித் திட்டங்கள்",
        "training_description": (
            "தற்போதைய வேளாண் திட்டத் தகவல்களில் உள்ள "
            "விவசாயிகள் பயிற்சி விவரங்களைப் பாருங்கள்."
        ),
        "training_contact": (
            "பயிற்சி தேதிகள், இடங்கள் மற்றும் பதிவு விவரங்களுக்கு "
            "அருகிலுள்ள வேளாண் பொறியியல் துறை அலுவலகத்தை அணுகவும்."
        ),
        "no_training": (
            "தற்போதைய திட்டத் தகவல்களில் தனிப்பட்ட பயிற்சித் "
            "திட்ட விவரங்கள் எதுவும் கிடைக்கவில்லை."
        ),
    },
}

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #10251b;
        color: #e8f1e9;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #142f22;
        border-right: 1px solid #31533c;
    }

    [data-testid="stSidebar"] * {
        color: #e8f1e9;
    }

    h1, h2, h3 {
        color: #f0fff3 !important;
    }

    p, label, li {
        color: #d4e5d7;
    }

    .hero {
        background: linear-gradient(135deg, #245b37, #163b29);
        border: 1px solid #477653;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 22px;
    }

    .hero-kicker {
        color: #b9e7c5;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: 34px;
        margin: 12px 0;
    }

    .hero p {
        color: #d8eadc;
        font-size: 16px;
        margin-bottom: 0;
    }

    .metric-card {
        background: #1b3829;
        border: 1px solid #41664c;
        border-radius: 15px;
        padding: 18px;
        min-height: 105px;
    }

    .metric-label {
        color: #b8d5bf;
        font-size: 13px;
    }

    .metric-value {
        color: #f2fff4;
        font-size: 25px;
        font-weight: 700;
        margin-top: 8px;
    }

    .disclaimer {
        background: #2c3825;
        border-left: 4px solid #d9ad50;
        border-radius: 8px;
        padding: 13px;
        color: #f1e5c4;
        font-size: 13px;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #9bb9a2;
        font-size: 12px;
        padding: 25px 0 5px 0;
    }

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #5d956b;
        background: #28613b;
        color: white;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #34794b;
        color: white;
        border-color: #8bc69a;
    }

    [data-testid="stChatMessage"] {
        background: #1b3829;
        border: 1px solid #355b40;
        border-radius: 12px;
    }

    [data-testid="stExpander"] {
        border: 1px solid #41664c;
        border-radius: 10px;
    }

    a {
        color: #9fddb0 !important;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 20px;
        }

        .hero h1 {
            font-size: 25px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_value(data, possible_keys, default=""):
    if not isinstance(data, dict):
        return default

    for key in possible_keys:
        value = data.get(key)
        if value is not None and value != "":
            return value

    return default


def clean_source_text(text):
    if isinstance(text, dict):
        text = (
            text.get("page_content")
            or text.get("text")
            or text.get("content")
            or str(text)
        )

    if isinstance(text, list):
        return "\n".join(clean_source_text(item) for item in text)

    if text is None:
        return ""

    return re.sub(r"\s+", " ", str(text)).strip()


def answer_to_text(answer):
    if isinstance(answer, list):
        parts = []

        for item in answer:
            if isinstance(item, dict):
                value = (
                    item.get("text")
                    or item.get("content")
                    or item.get("answer")
                    or ""
                )
                if value:
                    parts.append(str(value))
            else:
                parts.append(str(item))

        return "\n\n".join(parts)

    if isinstance(answer, dict):
        return clean_source_text(answer)

    return str(answer or "No answer was returned.")


def display_sources(sources, t):
    if not sources:
        return

    st.markdown(f"#### {t['sources']}")

    for index, source in enumerate(sources, start=1):

        if isinstance(source, str):
            source_name = source
            source_text = ""
            score = None
            page = None
            url = None

        elif isinstance(source, dict):
            source_name = get_value(
                source,
                ["source", "source_name", "file_name", "filename", "title"],
                f"Source {index}",
            )

            source_text = get_value(
                source,
                ["text", "page_content", "content", "excerpt"],
                "",
            )

            score = source.get("score")
            page = source.get("page")
            url = source.get("url")

        else:
            source_name = f"Source {index}"
            source_text = str(source)
            score = None
            page = None
            url = None

        with st.container(border=True):
            st.markdown(f"**{index}. {source_name}**")

            if page:
                st.caption(f"Page: {page}")

            if score is not None:
                st.caption(f"Relevance score: {score}")

            if source_text:
                st.write(clean_source_text(source_text)[:1200])

            if url:
                st.markdown(f"[Open source]({url})")


def get_scheme_data():
    try:
        response = requests.get(
            f"{API_URL}/schemes",
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return (
                data.get("schemes")
                or data.get("data")
                or data.get("results")
                or []
            )

        return []

    except requests.exceptions.RequestException as error:
        st.error(
            "Unable to connect to the backend. "
            "Please check that the FastAPI server is running."
        )
        st.caption(str(error))
        return []


def display_scheme(scheme, index, t):
    name = get_value(
        scheme,
        ["scheme_name", "name", "title", "scheme"],
        f"Agricultural Scheme {index}",
    )

    description = get_value(
        scheme,
        ["description", "scheme_description", "details"],
        "No description available.",
    )

    subsidy = get_value(
        scheme,
        ["subsidy", "subsidy_details", "financial_assistance", "benefit"],
        "Please refer to the scheme details.",
    )

    eligibility = get_value(
        scheme,
        ["eligibility", "eligible_farmers", "beneficiary"],
        "Please contact the relevant department for eligibility details.",
    )

    project_area = get_value(
        scheme,
        ["project_area", "area", "location"],
        "Please check with the relevant department.",
    )

    application = get_value(
        scheme,
        ["application_process", "how_to_apply", "application"],
        "Contact the relevant Agriculture Department office.",
    )

    with st.expander(f"🌱 {name}", expanded=False):

        st.markdown(f"**{t['about']}**")
        st.write(clean_source_text(description))

        st.markdown(f"**{t['subsidy']}**")
        st.write(clean_source_text(subsidy))

        st.markdown(f"**{t['eligibility']}**")
        st.write(clean_source_text(eligibility))

        st.markdown(f"**{t['project_area']}**")
        st.write(clean_source_text(project_area))

        st.markdown(f"**{t['application']}**")
        st.write(clean_source_text(application))


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🌾 Scheme Assistant")
    st.caption("Tamil Nadu Agricultural Scheme AI")

    language = st.selectbox(
        "🌐 Select Language / மொழியைத் தேர்ந்தெடுக்கவும்",
        ["English", "தமிழ்"],
        key="app_language",
    )

    t = TEXT[language]

    st.divider()

    st.markdown(f"### {t['pdf']}")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload an agricultural scheme PDF for the chatbot.",
    )

    if uploaded_file is not None:

        if st.button(t["upload"], use_container_width=True):

            with st.spinner("Uploading and processing PDF..."):

                try:
                    response = requests.post(
                        f"{API_URL}/upload-pdf",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf",
                            )
                        },
                        timeout=300,
                    )

                    if response.ok:
                        st.success(t["upload_success"])
                        st.json(response.json())
                    else:
                        st.error(f"Upload failed: {response.status_code}")
                        st.write(response.text)

                except requests.exceptions.RequestException as error:
                    st.error(f"Backend connection error: {error}")

    st.divider()

    st.markdown(f"### {t['tnau']}")

    if st.button(t["update"], use_container_width=True):

        with st.spinner("Fetching TNAU website data..."):

            try:
                response = requests.post(
                    f"{API_URL}/ingest-tnau",
                    timeout=300,
                )

                if response.ok:
                    st.success(t["update_success"])
                    st.json(response.json())
                else:
                    st.error(f"Update failed: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.RequestException as error:
                st.error(f"Backend connection error: {error}")

    st.markdown(f"[Visit TNAU Website]({TNAU_URL})")

    st.divider()

    if st.button(t["clear"], use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.divider()
    st.caption("Powered by FastAPI • Streamlit • RAG")

# --------------------------------------------------
# MAIN HOMEPAGE
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">
            Tamil Nadu Agriculture • AI Assistant
        </div>
        <h1>🌾 உழவனின் உரிமைக்கரம்</h1>
        <p>
            Agricultural Scheme AI Assistant
            <br>
            Discover government schemes, understand subsidies,
            and get agricultural information in simple language.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

schemes = get_scheme_data()

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{t['available']}</div>
            <div class="metric-value">{len(schemes)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{t['information']}</div>
            <div class="metric-value">AI Powered</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{t['knowledge']}</div>
            <div class="metric-value">PDF + TNAU</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------
# MAIN TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        t["explorer"],
        t["chatbot"],
        t["training"],
    ]
)

# ==================================================
# TAB 1 — SCHEME EXPLORER
# ==================================================

with tab1:

    st.markdown(f"### {t['explore_heading']}")
    st.write(t["explore_description"])

    if schemes:

        search_text = st.text_input(
            t["search"],
            placeholder=t["search_placeholder"],
            key="scheme_search",
        )

        all_districts = set()

        for scheme in schemes:

            districts = get_value(
                scheme,
                ["districts", "district"],
                [],
            )

            if isinstance(districts, str):
                districts = [districts]

            if isinstance(districts, list):
                for district in districts:
                    if district:
                        all_districts.add(str(district))

        district_options = [
            t["all_districts"]
        ] + sorted(all_districts)

        selected_district = st.selectbox(
            t["district"],
            district_options,
            key="district_filter",
        )

        filtered_schemes = []

        for scheme in schemes:

            searchable_text = " ".join(
                str(value)
                for value in scheme.values()
                if value is not None
            ).lower()

            if search_text.lower() not in searchable_text:
                continue

            if selected_district != t["all_districts"]:

                districts = get_value(
                    scheme,
                    ["districts", "district"],
                    [],
                )

                if isinstance(districts, str):
                    districts = [districts]

                if selected_district not in [
                    str(district) for district in districts
                ]:
                    continue

            filtered_schemes.append(scheme)

        st.caption(
            f"{t['showing']} {len(filtered_schemes)} "
            f"{t['of']} {len(schemes)} {t['schemes']}"
        )

        if filtered_schemes:

            for index, scheme in enumerate(filtered_schemes, start=1):
                display_scheme(scheme, index, t)

        else:
            st.info(t["no_schemes"])

    else:
        st.warning(
            "No scheme information is currently available. "
            "Please check the backend."
        )

    st.markdown(
        f"""
        <div class="disclaimer">
            <b>{t['important']}</b> {t['disclaimer']}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==================================================
# TAB 2 — AI CHATBOT
# ==================================================

with tab2:

    st.markdown(f"### {t['chat_heading']}")
    st.write(t["chat_description"])

    st.markdown(f"**{t['try_asking']}**")

    example_questions = t["examples"]
    example_columns = st.columns(3)

    for index, question in enumerate(example_questions):

        with example_columns[index]:

            if st.button(
                f"{t['example_label']} {index + 1}",
                use_container_width=True,
                key=f"example_{index}",
            ):
                st.session_state.pending_question = question
                st.rerun()

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("sources"):
                display_sources(message["sources"], t)

    user_question = st.chat_input(t["chat_placeholder"])

    question = (
        st.session_state.pending_question
        or user_question
    )

    if question:

        st.session_state.pending_question = None

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Finding the best answer..."):

                try:
                    question_for_ai = (
                        question
                        + "\n\n"
                        + t["answer_language"]
                    )

                    response = requests.post(
                        f"{API_URL}/ask",
                        params={"question": question_for_ai},
                        timeout=180,
                    )

                    response.raise_for_status()
                    result = response.json()

                    answer = answer_to_text(
                        result.get("answer", result)
                    )

                    sources = (
                        result.get("sources")
                        or result.get("source_documents")
                        or []
                    )

                    st.markdown(answer)

                    if sources:
                        display_sources(sources, t)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                except requests.exceptions.RequestException as error:

                    error_message = (
                        "I could not connect to the backend. "
                        "Please check that the FastAPI server is running."
                    )

                    st.error(error_message)
                    st.caption(str(error))

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

                except Exception as error:

                    error_message = (
                        "Something went wrong while processing your question."
                    )

                    st.error(error_message)
                    st.caption(str(error))

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

# ==================================================
# TAB 3 — TRAINING PROGRAMMES
# ==================================================

with tab3:

    st.markdown(f"### {t['training_heading']}")
    st.write(t["training_description"])

    training_schemes = []

    for scheme in schemes:

        scheme_name = clean_source_text(
            get_value(
                scheme,
                ["scheme_name", "name", "title", "scheme"],
                "",
            )
        )

        if "training" in scheme_name.lower():
            training_schemes.append(scheme)

    if training_schemes:

        for index, scheme in enumerate(training_schemes, start=1):

            display_scheme(scheme, index, t)

    else:

        st.info(t["no_training"])

    st.markdown(
        f"""
        <div class="disclaimer">
            {t['training_contact']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"[Visit TNAU Website]({TNAU_URL})"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    f"""
    <div class="footer">
        🌾 உழவனின் உரிமைக்கரம்
        <br>
        {t['assistant']}
        <br>
        {t['powered']}
    </div>
    """,
    unsafe_allow_html=True,
)
