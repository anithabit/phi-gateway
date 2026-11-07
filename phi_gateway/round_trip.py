from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

NOTE = """Call 555-246-8135 or (555) 246-8135 or 5552468135 or 555.246.8135.
Also +1 555 246 8135 and 555 246 8135 ext. 12.
BP 120/80, Hb 12.5, 3 days post-op, diagnosed in 2019."""

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