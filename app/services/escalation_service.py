import uuid
from app.database import save_escalation
from app.config import settings

def trigger_escalation(session_id: str, user_id: str, reason: str, score: float) -> str:
    ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
    urgency = "HIGH" if score >= 0.8 else "MEDIUM"
    save_escalation(ticket_id, session_id, user_id, reason, urgency)
    
    # In production, dispatch email or webhook
    # For audit/logging:
    print(f"[ESCALATION TRIGGERED] Ticket {ticket_id} created for session {session_id} (Reason: {reason}, Urgency: {urgency})")
    return ticket_id
