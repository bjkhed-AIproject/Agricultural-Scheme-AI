
import json
import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

INPUT_PATH = "data/scheme_sections.json"
OUTPUT_PATH = "data/schemes.json"

SOURCE_URL = (
    "https://agritech.tnau.ac.in/agricultural_engineering/"
    "agriengg_govt_schemes.html"
)


def create_ai_model():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key,
        temperature=0
    )


def extract_json(response):

    content = response.content

    if isinstance(content, list):
        content = "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = str(content).strip()

    content = re.sub(
        r"^```(?:json)?\s*",
        "",
        content
    )

    content = re.sub(
        r"\s*```$",
        "",
        content
    )

    return json.loads(content)


def extract_one_scheme(llm, section):

    prompt = f"""
You are extracting information from an official
Tamil Nadu Agricultural Engineering Department webpage.

Extract information ONLY for Scheme Number
{section['scheme_number']}.

Return ONLY valid JSON in this structure:

{{
  "scheme_number": {section['scheme_number']},
  "name": "Official scheme name",
  "category": null,
  "description": null,
  "project_area": null,
  "subsidy": null,
  "eligibility": null,
  "how_to_apply": null,
  "required_documents": [],
  "districts": [],
  "benefit_type": null,
  "contact_office": null,
  "application_url": "{SOURCE_URL}"
}}

STRICT RULES:

1. Use ONLY the supplied scheme section.
2. Do not use information from other schemes.
3. Never invent subsidy percentages or amounts.
4. Preserve important conditions and beneficiary contributions.
5. If information is missing, use null.
6. Do not interpret missing subsidy information as zero subsidy.
7. Keep the official scheme name as accurately as possible.
8. Do not invent application procedures or documents.
9. Keep project area and eligibility separate.
10. Return valid JSON only.

SCHEME SECTION:

{section['raw_text']}
"""

    response = llm.invoke(prompt)

    return extract_json(response)


def build_scheme_catalogue():

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        sections = json.load(file)

    llm = create_ai_model()

    schemes = []

    for section in sections:

        number = section["scheme_number"]

        print(f"Processing Scheme {number} of 15...")

        try:

            scheme = extract_one_scheme(
                llm,
                section
            )

            scheme["scheme_number"] = number
            scheme["source"] = "TNAU Agricultural Engineering Department"
            scheme["source_url"] = SOURCE_URL

            # Preserve original text for verification.
            scheme["original_source_text"] = section["raw_text"]

            schemes.append(scheme)

            print("Successfully extracted:", scheme.get("name"))

        except Exception as error:

            print(f"Scheme {number} extraction failed: {error}")

            schemes.append({
                "scheme_number": number,
                "name": f"Scheme No. {number}",
                "category": None,
                "description": None,
                "project_area": None,
                "subsidy": None,
                "eligibility": None,
                "how_to_apply": None,
                "required_documents": [],
                "districts": [],
                "benefit_type": None,
                "contact_office": None,
                "application_url": SOURCE_URL,
                "source": "TNAU Agricultural Engineering Department",
                "source_url": SOURCE_URL,
                "original_source_text": section["raw_text"],
                "extraction_status": "Needs verification"
            })

    os.makedirs("data", exist_ok=True)

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schemes,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nCATALOGUE GENERATION COMPLETED")
    print("Total scheme sections:", len(schemes))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":

    build_scheme_catalogue()
