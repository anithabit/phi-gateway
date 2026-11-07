import re
PATTERNS = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "PHONE": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "ZIP": r"\b\d{5}(-\d{4})?\b",
    "URL": r"https?://\S+|www\.\S+",
    "IP": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "DATE": r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    "MRN": r"(?<=MRN: )\d+|(?<=MRN:)\d+|(?<=MRN )\d+",
}


def find_phi(text):
    found = []
    for label, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            found.append((match.start(), match.end(), label, match.group()))
    found.sort()
    return found


if __name__ == "__main__":
    note = "Call (555) 123-4567 or 555.987.6543, email jo.smith@mail.com. BP 120/80. 5551234567"
    for item in find_phi(note):
        print(item)