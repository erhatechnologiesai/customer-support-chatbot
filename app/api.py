from fastapi import FastAPI, HTTPException
from app.config import settings
from app.models import ChatRequest, ChatResponse, EscalationTicket
from app.database import init_db, save_message, get_history, search_faqs
from app.services.sentiment_service import analyze_sentiment
from app.services.escalation_service import trigger_escalation
from app.services.llm_service import generate_ai_reply
import sqlite3

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade AI Customer Support Chatbot API with sentiment scoring and automated human escalation."
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_msg = request.message.strip()
    
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    save_message(session_id, "user", user_msg)
    history = get_history(session_id)
    
    sentiment = analyze_sentiment(user_msg)
    escalated = False
    
    if sentiment >= settings.FRUSTRATION_THRESHOLD:
        escalated = True
        ticket_id = trigger_escalation(
            session_id=session_id,
            user_id=request.user_id or "anonymous",
            reason=f"High frustration sentiment ({sentiment}) detected in message: '{user_msg[:50]}...'",
            score=sentiment
        )
        reply = (
            f"I detect that this is an urgent matter. I have immediately opened priority support ticket #{ticket_id} "
            f"and notified a human specialist. In the meantime, I'm here if you have additional details to share."
        )
        sources = ["Human Escalation System"]
    else:
        reply, sources = generate_ai_reply(user_msg, history)
        
    save_message(session_id, "assistant", reply)
    
    return ChatResponse(
        session_id=session_id,
        reply=reply,
        escalated=escalated,
        sentiment_score=sentiment,
        sources=sources
    )

@app.get("/history/{session_id}")
def get_session_history(session_id: str):
    history = get_history(session_id, limit=50)
    return {"session_id": session_id, "messages": history}

@app.get("/escalations")
def list_escalations():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ticket_id, session_id, user_id, reason, urgency, status, created_at FROM escalations ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "ticket_id": r[0],
            "session_id": r[1],
            "user_id": r[2],
            "reason": r[3],
            "urgency": r[4],
            "status": r[5],
            "created_at": r[6]
        }
        for r in rows
    ]
