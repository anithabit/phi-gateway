# PHI De-identification Gateway

Masks patient identifiers in clinical notes before they are sent to an LLM,
then restores them in the LLM's reply.

## Setup

(to do)

## Results (baseline)

Test set: 20 hand-labelled notes, 111 identifiers.

| System | Precision | Recall | Leak rate |
|---|---|---|---|
| Regex only | 0.97 | 0.29 | 100% |
| Presidio | 0.47 | 0.63 | 80% |

- Regex: precise, but finds no names or places.
- Presidio: finds names, but masks relative times ("3 days ago") and misses MRN/ZIP.

## Sources and tools used

- Project brief from LezdoTechMed
- Python `re` docs: https://docs.python.org/3/library/re.html
- regex101.com for testing patterns
- Groq API (free tier): https://console.groq.com
- Groq model deprecations: https://console.groq.com/docs/deprecations
- Microsoft Presidio: https://microsoft.github.io/presidio/
- spaCy en_core_web_lg
