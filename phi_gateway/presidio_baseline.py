from presidio_analyzer import AnalyzerEngine

from phi_gateway.evaluate import load_notes, evaluate, show

TYPE_MAP = {
    "PERSON": "NAME",
    "LOCATION": "LOCATION",
    "DATE_TIME": "DATE",
    "PHONE_NUMBER": "PHONE",
    "EMAIL_ADDRESS": "EMAIL",
    "US_SSN": "SSN",
    "URL": "URL",
    "IP_ADDRESS": "IP",
    "MEDICAL_LICENSE": "ID",
    "US_DRIVER_LICENSE": "ID",
    "US_BANK_NUMBER": "ID",
}

analyzer = AnalyzerEngine()


def presidio_find(text):
    found = []
    for r in analyzer.analyze(text=text, language="en"):
        label = TYPE_MAP.get(r.entity_type, "OTHER")
        found.append((r.start, r.end, label, text[r.start:r.end]))
    return found


if __name__ == "__main__":
    notes = load_notes("data/test_notes.txt")
    stats, leaked = evaluate(notes, detector=presidio_find)
    show(stats, leaked, len(notes))