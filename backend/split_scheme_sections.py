
import re
import json
import os

INPUT_FILE = "data/original_pdf_text.txt"
OUTPUT_FILE = "data/scheme_sections.json"


def split_schemes():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    pattern = r"(?im)^\s*[‘'`]?SCHEME\s+NO\.?\s*(\d{1,2})\b"

    matches = list(re.finditer(pattern, text))

    schemes = []

    for index, match in enumerate(matches):

        scheme_number = int(match.group(1))

        start = match.start()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        schemes.append({
            "scheme_number": scheme_number,
            "raw_text": section_text
        })

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            schemes,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Scheme separation completed!")
    print("Total scheme sections:", len(schemes))
    print("Saved to:", OUTPUT_FILE)

    print("\nScheme numbers found:")

    for scheme in schemes:
        print("Scheme No.", scheme["scheme_number"])


if __name__ == "__main__":
    split_schemes()
