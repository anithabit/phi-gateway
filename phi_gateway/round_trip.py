import sys
import textwrap

from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

NOTE = """Patient Meena Raghavan was seen on 03/14/2025 at City Hospital.
Her husband Ravi called from 555-246-8135. Dr. James Parkinson confirmed Parkinson's disease.
She is 67 years old. Pain started 3 days ago."""

INSTRUCTION = (
    "Summarise the clinical note below in 2 sentences. "
    "Keep every placeholder such as [PHONE_1] exactly as written.\n\n"
)


def show(title, text):
    print("\n" + title)
    for line in text.splitlines():
        print(textwrap.fill(line, width=90, break_on_hyphens=False, break_long_words=False))


def round_trip(note):
    masked, mapping = deidentify(note)
    show("1. MASKED NOTE SENT TO LLM:", masked)

    reply = ask_llm(INSTRUCTION + masked)
    show("2. RAW LLM REPLY:", reply)

    restored = rehydrate(reply, mapping)
    show("3. RESTORED REPLY:", restored)
    return restored


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            round_trip(f.read())
    else:
        round_trip(NOTE)