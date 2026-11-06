import re

from phi_gateway.regex_detector import find_phi


def deidentify(text):
    mapping = {}
    counters = {}

    for start, end, label, value in find_phi(text):
        if value in mapping.values():
            continue
        counters[label] = counters.get(label, 0) + 1
        placeholder = f"[{label}_{counters[label]}]"
        mapping[placeholder] = value

    masked_text = text
    for placeholder, value in mapping.items():
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