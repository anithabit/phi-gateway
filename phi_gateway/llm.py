import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

CLEAN = {
    "\u2010": "-", "\u2011": "-", "\u2013": "-", "\u2014": "-",
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u00a0": " ",
}


def clean_text(text):
    for bad, good in CLEAN.items():
        text = text.replace(bad, good)
    return text


def ask_llm(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(GROQ_URL, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    return clean_text(response.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    print(ask_llm("Say hello in five words."))