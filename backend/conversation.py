import os, requests, json

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
SYSTEM_PROMPT = os.getenv("ASSISTANT_SYSTEM_PROMPT", "You are a supportive onboard assistant for astronauts.")

def chat(messages: list[dict]) -> str:
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {"model": OLLAMA_MODEL, "messages": messages, "stream": False}
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]