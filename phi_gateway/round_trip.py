from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

NOTE = """Patient seen on 03/14/2025. MRN: 00123456. Lives near Boston 02115.
Contact daughter at 555-999-1111 or anna.r@example.com. SSN: 123-45-6789.
Portal: https://portal.example.org/p/12 (login from 192.168.1.10).
Wound check 3 days post-op. BP 120/80."""

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