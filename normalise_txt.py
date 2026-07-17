import re
from pathlib import Path

# DOCX Support
from docx import Document




class DocumentProcessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = Path(file_path).suffix.lower()

    # -----------------------------
    # DOCX Extraction
    # -----------------------------
    def extract_docx(self):

        doc = Document(self.file_path)

        text_parts = []

        for para in doc.paragraphs:

            if para.text.strip():
                text_parts.append(para.text)

        return "\n".join(text_parts)

    # -----------------------------
    # Fix Vertical Text
    # -----------------------------
    def fix_vertical_text(self, text):

        lines = text.splitlines()

        result = []
        current_word = []

        for line in lines:

            line = line.strip()

            if len(line) == 1 and line.isalpha():

                current_word.append(line)

            else:

                if current_word:

                    result.append("".join(current_word))
                    current_word = []

                result.append(line)

        if current_word:
            result.append("".join(current_word))

        return "\n".join(result)

    # -----------------------------
    # General Cleanup
    # -----------------------------
    def normalize_text(self, text):

        # Remove strange PDF chars
        text = text.replace("￾", "")
        text = text.replace("\ufeff", "")

        # Fix vertical text
        text = self.fix_vertical_text(text)

        # Normalize whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Remove repeated blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Trim spaces around lines
        text = "\n".join(
            line.strip()
            for line in text.splitlines()
        )

        return text.strip()

    # -----------------------------
    # Main Pipeline
    # -----------------------------
    def process(self):

        if self.extension == ".docx":

            raw_text = self.extract_docx()

        else:

            raise ValueError(
                f"Unsupported file type: {self.extension}"
            )

        normalized_text = self.normalize_text(raw_text)

        return normalized_text


if __name__ == "__main__":

    INPUT_FILE = "input/Red Herring Prospectus.docx"
    OUTPUT_FILE = "output/normalized_text.txt"

    processor = DocumentProcessor(INPUT_FILE)

    clean_text = processor.process()