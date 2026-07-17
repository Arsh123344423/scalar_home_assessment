from PII_detector import detect_pii
from redactor import redact_text, replacement_map
import normalise_txt
from redactor_dox import redact_docx
input_file = "input/Red Herring Prospectus.docx"

# Extract text
clean_text = normalise_txt.DocumentProcessor(
    input_file
).process()

# Detect PII
entities = detect_pii(clean_text)

# Build replacement map + redacted text
redacted_text = redact_text(
    clean_text,
    entities
)

# Save formatted DOCX
redact_docx(
    input_file,
    "output/redacted.docx"
)