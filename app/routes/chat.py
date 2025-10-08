from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.profile_store import profile_store
from app.llm import generate
from app.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])

SYSTEM_PROMPT = (
    "You are an assistant that answers questions about Gowtham Chandrasekaran. "
    "Always write in the third person (he/him/his); never say 'I' or 'me'. "
    "Use only the PROFILE facts. If the question is unrelated to his professional background "
    "(e.g., personal relationships, unrelated trivia, or general chit-chat), reply with: "
    f"'{settings.FALLBACK_MESSAGE}'. "
    "Be concise (3–6 sentences). Do not invent details."
)


def build_user_prompt(profile_text: str, question: str) -> str:
    return (
        "PROFILE (authoritative facts about Gowtham):\n"
        "-------------------------------------------\n"
        f"{profile_text}\n"
        "-------------------------------------------\n\n"
        "INSTRUCTIONS:\n"
        "- Answer only from PROFILE.\n"
        "- If PROFILE lacks the info, say you're unsure.\n"
        "- Keep third person tone.\n\n"
        f"QUESTION: {question}\n"
    )

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    question = next((m.content.strip() for m in reversed(req.messages) if m.role == "user"), "")
    if not question:
        raise HTTPException(status_code=400, detail="No user message provided.")

    profile_text = profile_store.load()

    try:
        answer = await generate(SYSTEM_PROMPT, build_user_prompt(profile_text, question))
    except Exception:
        answer = "I’m unsure right now."

    # In prompt-only mode, profile.md is the sole source.
    sources = [Source(title="Profile", location="app/content/profile.md", snippet="Canonical profile facts.")]
    return ChatResponse(answer=answer, sources=sources)
