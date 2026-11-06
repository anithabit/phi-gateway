from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

NOTE = """Patient seen today. Contact daughter at 555-999-1111 or anna.r@mail.com.
If no answer, try 555-999-1111 again or the clinic line 555-777-1200. Backup: 5551234567."""

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