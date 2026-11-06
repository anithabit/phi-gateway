import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

def ask_llm(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(GROQ_URL, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(ask_llm("Say hello in five words."))