import re

from phi_gateway.evaluate import load_notes
from phi_gateway.gateway import deidentify, rehydrate
from phi_gateway.llm import ask_llm

QUESTION = (
    "Read the clinical note below. In 2 short sentences, give the main medical problem and the plan. "
    "Keep every placeholder such as [NAME_1] exactly as written.\n\n"
)


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def overlap(a, b):
    return len(words(a) & words(b)) / len(words(a) | words(b))


if __name__ == "__main__":
    notes = load_notes("data/test_notes.txt")[:5]
    lines = ["# Utility check: original vs masked notes\n"]
    scores = []
    baselines = []

    for i, (text, gold) in enumerate(notes, 1):
        original_answer = ask_llm(QUESTION + text)
        original_again = ask_llm(QUESTION + text)

        masked, mapping = deidentify(text)
        masked_answer = rehydrate(ask_llm(QUESTION + masked), mapping)

        baseline = overlap(original_answer, original_again)
        score = overlap(original_answer, masked_answer)
        scores.append(score)
        baselines.append(baseline)
        print(f"Note {i}: masked {score:.2f}   original-vs-original {baseline:.2f}")

        lines.append(f"## Note {i} (masked {score:.2f}, original-vs-original {baseline:.2f})\n")
        lines.append(f"**Original answer:** {original_answer}\n")
        lines.append(f"**Masked answer (restored):** {masked_answer}\n")

    average = sum(scores) / len(scores)
    average_baseline = sum(baselines) / len(baselines)
    print(f"Average masked: {average:.2f}")
    print(f"Average original-vs-original: {average_baseline:.2f}")
    lines.append(f"\n**Average masked: {average:.2f}. Average original-vs-original: {average_baseline:.2f}**\n")

    with open("utility_check.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to utility_check.md")