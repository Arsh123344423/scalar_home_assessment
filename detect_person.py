import re

def person_regex_detect(text):

    entities = []

    pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'

    for match in re.finditer(pattern, text):

        entities.append({
            "source": "person_regex",
            "type": "PERSON",
            "text": match.group(),
            "start": match.start(),
            "end": match.end(),
            "score": 0.85
        })

    return entities