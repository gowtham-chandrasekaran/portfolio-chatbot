from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.routes import chat
from app.config import settings
from app.profile_store import profile_store

app = FastAPI(title="Portfolio Chatbot (Prompt-only)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list(),
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}

@app.post("/admin/reload-profile")
def reload_profile():
    text = profile_store.refresh()
    return {"ok": True, "chars": len(text)}

app.include_router(chat.router)

# helpful sanity check: ping Groq
@app.get("/admin/ping-groq")
async def ping_groq():
    from app.llm import generate
    txt = await generate("Answer in one short sentence.", "Say: Groq is reachable.")
    return {"ok": True, "text": txt}
