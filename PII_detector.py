import re
import spacy
import json
import normalise_txt
from presidio_analyzer import AnalyzerEngine

# --------------------------------------------------
# Load Models
# --------------------------------------------------

nlp = spacy.load("en_core_web_lg")
analyzer = AnalyzerEngine()

# --------------------------------------------------
# Regex Patterns
# --------------------------------------------------

REGEX_PATTERNS = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "PHONE": r"(?:\+91[\s\-]?)?[6-9]\d{9}",
    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "DOB": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
}

# --------------------------------------------------
# Presidio Detection
# --------------------------------------------------

def presidio_detect(text):
    results = analyzer.analyze(text=text, language="en")
    entities = []
    for r in results:
        entities.append({
            "source": "presidio",
            "type": r.entity_type,
            "text": text[r.start:r.end],
            "start": r.start,
            "end": r.end,
            "score": round(r.score, 3)
        })
    return entities

# --------------------------------------------------
# Regex Detection
# --------------------------------------------------

def regex_detect(text):
    entities = []
    for entity_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            entities.append({
                "source": "regex",
                "type": entity_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "score": 1.0
            })
    return entities

# --------------------------------------------------
# spaCy Detection
# --------------------------------------------------

IGNORE_PERSONS = {
    "email", "email:", "e-mail", "e-mail:", "phone", "phone:", "mobile", "mobile:",
    "address", "address:", "contact", "contact:", "website", "website:", "fax", "fax:",
    "Telephone", "Telephone:"
}

SPACY_MAPPING = {
    "PERSON": "PERSON",
    "ORG": "ORGANIZATION",
    "GPE": "LOCATION",
    "LOC": "LOCATION"
}

PERSON_NAME_PATTERN = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b"


def spacy_detect(text):
    doc = nlp(text)
    entities = []

    for match in re.finditer(PERSON_NAME_PATTERN, text):
        entities.append({
            "source": "spacy",
            "type": "PERSON",
            "text": match.group(),
            "start": match.start(),
            "end": match.end(),
            "score": 0.90
        })

    for ent in doc.ents:
        if ent.label_ not in SPACY_MAPPING:
            continue
        if ent.label_ == "PERSON" and ent.text.strip().lower() in IGNORE_PERSONS:
            continue
        entities.append({
            "source": "spacy",
            "type": SPACY_MAPPING[ent.label_],
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "score": 0.90
        })
    return entities

# --------------------------------------------------
# Merge Duplicates
# --------------------------------------------------

def merge_entities(entity_list):
    seen = set()
    merged = []
    for entity in entity_list:
        key = (entity["text"].strip(), entity["type"])
        if key not in seen:
            seen.add(key)
            merged.append(entity)
    return merged

# --------------------------------------------------
# Main Detection Function
# --------------------------------------------------

def detect_pii(text):
    entities = []
    entities.extend(presidio_detect(text))
    entities.extend(regex_detect(text))
    entities.extend(spacy_detect(text))
    entities = merge_entities(entities)
    entities.sort(key=lambda x: x["start"])
    return entities

# --------------------------------------------------
# Save to JSON
# --------------------------------------------------

def save_to_json(entities, filename="predicted.json"):
    # Ensure all entities have required fields
    for entity in entities:
        if "start" not in entity:
            entity["start"] = 0
        if "end" not in entity:
            entity["end"] = 0
        if "score" not in entity:
            entity["score"] = 1.0
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(entities)} entities to {filename}")

# --------------------------------------------------
# Example Run
# --------------------------------------------------

if __name__ == "__main__":
    sample_text = normalise_txt.DocumentProcessor("input/Red Herring Prospectus.docx").process()

    entities = detect_pii(sample_text)

    print("\nDetected Entities\n")
    for entity in entities:
        print(
            f"[{entity['type']}] "
            f"{entity['text']} "
            f"({entity['source']})"
        )

    # Save predictions to JSON for recall calculation
    save_to_json(entities)