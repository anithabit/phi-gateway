from phi_gateway.regex_detector import find_phi


def deidentify(text):
    found = find_phi(text)
    mapping = {}
    value_to_placeholder = {}
    counters = {}
    pieces = []
    last_end = 0

    for start, end, label, value in found:
        if start < last_end:
            continue

        if value not in value_to_placeholder:
            counters[label] = counters.get(label, 0) + 1
            placeholder = f"[{label}_{counters[label]}]"
            value_to_placeholder[value] = placeholder
            mapping[placeholder] = value

        pieces.append(text[last_end:start])
        pieces.append(value_to_placeholder[value])
        last_end = end

    pieces.append(text[last_end:])
    masked_text = "".join(pieces)
    return masked_text, mapping


if __name__ == "__main__":
    note = "Call 555-123-4567 or email jo@mail.com. If no answer, call 555-123-4567 again or 555-999-0000."
    masked, mapping = deidentify(note)
    print(masked)
    print(mapping)