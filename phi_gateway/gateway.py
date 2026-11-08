import re

from phi_gateway.model_detector import combined_find


def deidentify(text):
    mapping = {}
    replacements = {}
    seen = {}
    counters = {}

    for start, end, label, value in combined_find(text, 0.2):
        key = label + ":" + re.sub(r"\W", "", value).lower()
        if key not in seen:
            counters[label] = counters.get(label, 0) + 1
            seen[key] = f"[{label}_{counters[label]}]"
            mapping[seen[key]] = value
        replacements[value] = seen[key]

    masked_text = text
    for value, placeholder in replacements.items():
        masked_text = masked_text.replace(value, placeholder)

    return masked_text, mapping


def rehydrate(response, mapping):
    for placeholder, value in mapping.items():
        response = response.replace(placeholder, value)

    for leftover in re.findall(r"\[[A-Z]+_\d+\]", response):
        print("WARNING: unknown placeholder", leftover)

    return response


if __name__ == "__main__":
    note = "Call 555-123-4567 or email jo@mail.com. If no answer, call 555-123-4567 again or 555-999-0000."
    masked, mapping = deidentify(note)
    print("MASKED: ", masked)
    print("MAPPING:", mapping)

    fake_llm_reply = "Please call the patient at [PHONE_1]. Backup: [PHONE_2]. Also try [PHONE_7]."
    print("RESTORED:", rehydrate(fake_llm_reply, mapping))