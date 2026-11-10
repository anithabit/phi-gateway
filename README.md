# PHI De-identification Gateway

Masks patient identifiers in clinical notes before they are sent to an LLM,
then restores them in the LLM's reply. The mapping stays on my machine and is never sent to the LLM.

## How it works

1. `deidentify(text)` finds identifiers with regex (phones, emails, SSN, MRN, ZIP, URL, IP, ages over 89)
   and a fine-tuned DistilBERT model (names, locations, dates, IDs). Each value gets a placeholder like `[NAME_1]`.
2. Only the masked note goes to the LLM (Groq, `openai/gpt-oss-120b`).
3. `rehydrate(reply, mapping)` puts the real values back. A placeholder that is not in the mapping is left as it is
   and a warning is printed. I never guess, because a wrong value could point to the wrong patient.

## Demo video and trained model

- Demo video (3:36): https://drive.google.com/file/d/1Qinq-YC7zR9Jnj_I2MsFaJCpMzFUzQpk/view?usp=sharing
- Trained model (v2, 241 MB): https://drive.google.com/file/d/1vB_XSvGB97Vcy_czVZsX_n9nVumPzUQn/view?usp=sharing
  Unzip it in the project folder so the files are in `models/phi-model/`. Then you can skip training.

## Setup

Python 3.12.

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

Create a `.env` file with your free Groq key:

    GROQ_API_KEY=your_key_here

Train the model (about 2 minutes on a free Colab T4 GPU):

    python -m phi_gateway.synth
    python -m phi_gateway.train

## One command to run

    python -m phi_gateway.round_trip sample_note.txt

Put any clinical note in a text file and pass its name. It prints the masked note, the LLM reply and the restored reply.

Other commands:

    python -m phi_gateway.model_detector data/test_notes.txt 0.2   # model + regex results
    python -m phi_gateway.evaluate                                  # regex only
    python -m phi_gateway.presidio_baseline                         # Presidio
    python -m phi_gateway.utility_check                             # LLM answers, original vs masked

## Data

- `data/train_notes.txt`: 3000 synthetic notes made with Faker (`phi_gateway/synth.py`). No real patient data.
- `data/test_notes.txt`: 20 hand-labelled test notes, 111 identifiers.
- `data/dev_notes.txt`: 5 dev notes, used only to choose the threshold.

## Results

Test set: 20 hand-labelled notes, 111 identifiers. Leak rate = share of notes with at least one missed identifier.

| System | Precision | Recall | Leak rate |
|---|---|---|---|
| Regex only | 0.97 | 0.32 | 100% |
| Presidio | 0.47 | 0.63 | 80% |
| Model + regex (v1) | 0.54 | 0.64 | 50% |
| Model + regex (v2) | 0.68 | 0.82 | 25% |

Model: DistilBERT (`distilbert-base-cased`), 65,210,137 parameters.
Threshold 0.2, chosen on the dev set. v2 used better synthetic data (more locations, IDs and date formats),
based on dev-set errors.

Recall first: the model marks a word as an identifier if it is at least 20% sure, and regex results are always kept.
An extra mask is only an inconvenience; a missed one is a leak.

Utility check (5 notes): word overlap between the LLM's answers on original and masked notes was 0.57.
Two answers on the same original note overlapped 0.50, so masking did not lower answer quality. See `utility_check.md`.

## Special cases

- "Dr. Parkinson diagnosed Parkinson's disease": the name is masked, the disease is kept.
- Relative times like "3 days post-op" are kept; calendar dates are masked.
- Only ages over 89 are masked.
- The same value always gets the same placeholder, even in different formats (555-123-4567 and 5551234567).

## HIPAA Safe Harbor categories left out

- Full-face photos and biometric identifiers: the input is text only.
- Vehicle and device identifiers / serial numbers: rare in clinical notes and not in my training data.
  Other unique numbers are partly covered by the ID type.

## Known weaknesses

- Names are the weakest type (recall 0.70), especially lowercase or word-like names (Hope, Faith).
- The model over-marks some numbers as IDs.
- Test leak rate is still 25%, so this is not ready for real patient data.

## Sources and tools used

- Project brief from LezdoTechMed
- HHS guidance on HIPAA Safe Harbor de-identification
- Hugging Face Transformers and the token classification course chapter
- DistilBERT (`distilbert-base-cased`) on Hugging Face
- Google Colab (free T4 GPU) for training
- Faker for synthetic data
- Microsoft Presidio and spaCy `en_core_web_lg` for the baseline
- Groq API (free tier) and the Groq model deprecations page
- Python `re` docs and regex101.com
- youtube to refer and learn unknown concepts