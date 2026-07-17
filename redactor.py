from faker import Faker

fake = Faker()

# ---------------------------------------------------
# Global Mapping Storage
# ---------------------------------------------------

replacement_map = {}

person_map = {}

# ---------------------------------------------------
# Person
# ---------------------------------------------------

def fake_person(original):

    if original not in replacement_map:

        replacement_map[original] = fake.name()

    return replacement_map[original]


# ---------------------------------------------------
# Email
# ---------------------------------------------------

def fake_email(original):

    if original not in replacement_map:

        replacement_map[original] = fake.email()

    return replacement_map[original]


# ---------------------------------------------------
# Organization
# ---------------------------------------------------

def fake_company(original):

    if original not in replacement_map:

        replacement_map[original] = fake.company()

    return replacement_map[original]


# ---------------------------------------------------
# Address
# ---------------------------------------------------

def fake_address(original):

    if original not in replacement_map:

        replacement_map[original] = (
            fake.address()
            .replace("\n", ", ")
        )

    return replacement_map[original]


# ---------------------------------------------------
# Phone
# ---------------------------------------------------

def fake_phone(original):

    if original not in replacement_map:

        replacement_map[original] = "+91 9999999999"

    return replacement_map[original]


# ---------------------------------------------------
# IP Address
# ---------------------------------------------------

def fake_ip(original):

    if original not in replacement_map:

        replacement_map[original] = fake.ipv4()

    return replacement_map[original]


# ---------------------------------------------------
# Credit Card
# ---------------------------------------------------

def fake_card(original):

    if original not in replacement_map:

        replacement_map[original] = (
            fake.credit_card_number()
        )

    return replacement_map[original]


# ---------------------------------------------------
# SSN
# ---------------------------------------------------

def fake_ssn(original):

    if original not in replacement_map:

        replacement_map[original] = (
            "999-99-9999"
        )

    return replacement_map[original]


# ---------------------------------------------------
# Date of Birth
# ---------------------------------------------------

def fake_dob(original):

    if original not in replacement_map:

        replacement_map[original] = (
            "01/01/1990"
        )

    return replacement_map[original]


# ---------------------------------------------------
# Generic Dispatcher
# ---------------------------------------------------

def get_replacement(entity):

    entity_type = entity["type"]

    original = entity["text"]

    if entity_type == "PERSON":
        return fake_person(original)

    elif entity_type == "EMAIL_ADDRESS":
        return fake_email(original)

    elif entity_type == "ORGANIZATION":
        return fake_company(original)

    elif entity_type == "LOCATION":
        return fake_address(original)

    elif entity_type == "PHONE_NUMBER":
        return fake_phone(original)

    elif entity_type == "IP_ADDRESS":
        return fake_ip(original)

    elif entity_type == "CREDIT_CARD":
        return fake_card(original)

    elif entity_type == "SSN":
        return fake_ssn(original)

    elif entity_type == "DOB":
        return fake_dob(original)

    else:

        if original not in replacement_map:

            replacement_map[original] = (
                "[REDACTED]"
            )

        return replacement_map[original]


# ---------------------------------------------------
# Build Mapping
# ---------------------------------------------------

def build_mapping(entities):

    for entity in entities:

        get_replacement(entity)

    return replacement_map


# ---------------------------------------------------
# Redact Text
# ---------------------------------------------------

def redact_text(text, entities):

    entities = sorted(
        entities,
        key=lambda x: len(x["text"]),
        reverse=True
    )

    for entity in entities:

        original = entity["text"]

        replacement = get_replacement(entity)

        text = text.replace(
            original,
            replacement
        )

    return text
