from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

NOTE = """Patient Meena Raghavan was seen on 03/14/2025 at City Hospital.
Her husband Ravi called from 555-246-8135. Dr. James Parkinson confirmed Parkinson's disease.
She is 67 years old. Pain started 3 days ago."""

INSTRUCTION = (
    "Summarise the clinical note below in 2 sentences. "
    "Keep every placeholder such as [PHONE_1] exactly as written.\n\n"
)

def round_trip(note):
    masked, mapping = deidentify(note)
    print("1. MASKED NOTE SENT TO LLM:\n", masked)

    reply = ask_llm(INSTRUCTION + masked)
    print("\n2. RAW LLM REPLY:\n", reply)

    restored = rehydrate(reply, mapping)
    print("\n3. RESTORED REPLY:\n", restored)
    return restored

if __name__ == "__main__":
    round_trip(NOTE)