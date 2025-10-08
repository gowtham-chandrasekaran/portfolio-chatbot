import httpx
from app.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate(system_prompt: str, user_prompt: str) -> str:
    payload = {
        "model": settings.MODEL_NAME,            # e.g., "llama-3.1-70b-versatile"
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 512,                       # <-- REQUIRED by Groq
    }
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(GROQ_URL, headers=headers, json=payload)
        if r.status_code != 200:
            # show Groq’s actual error so we can diagnose fast
            raise RuntimeError(f"Groq error {r.status_code}: {r.text}")
        data = r.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            raise RuntimeError(f"Unexpected Groq response shape: {data}")
