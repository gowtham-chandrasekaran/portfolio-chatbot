from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    GROQ_API_KEY: str
    MODEL_NAME: str = "llama-3.1-70b-versatile"

    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]

    # app/config.py (add these fields inside Settings)
    FALLBACK_MESSAGE: str = (
        "Sorry—I can’t help with that. I can answer questions about Gowtham’s "
        "experience, projects, skills, education, and availability."
    )
    GREETING_MESSAGE: str = (
        "Hey there! You can ask about Gowtham’s experience, top projects, skills, "
        "education, or availability (visa, timelines). How can I help?"
    )


    # Helpers: allow ALLOWED_ORIGINS as JSON or comma-list
    def allowed_origins_list(self) -> List[str]:
        v = self.ALLOWED_ORIGINS
        if isinstance(v, list):
            return v
        s = v.strip()
        if s.startswith("["):
            try:
                arr = json.loads(s)
                if isinstance(arr, list):
                    return arr
            except Exception:
                pass
        return [x.strip() for x in s.split(",") if x.strip()]

settings = Settings()
