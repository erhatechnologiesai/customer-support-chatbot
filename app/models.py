from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    session_id: str
    user_id: Optional[str] = "guest"
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    escalated: bool = False
    sentiment_score: float
    sources: List[str] = []

class EscalationTicket(BaseModel):
    ticket_id: str
    session_id: str
    user_id: str
    reason: str
    urgency: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
