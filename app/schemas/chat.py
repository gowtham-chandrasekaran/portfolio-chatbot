from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class Source(BaseModel):
    title: str
    location: str
    snippet: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
