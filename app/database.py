import sqlite3
import json
from typing import List, Dict, Any
from app.config import settings

def init_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escalations (
            ticket_id TEXT PRIMARY KEY,
            session_id TEXT,
            user_id TEXT,
            reason TEXT,
            urgency TEXT,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faq_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            category TEXT
        )
    """)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM faq_items")
    if cursor.fetchone()[0] == 0:
        seed_faqs = [
            ("What is Erha Technologies?", "Erha Technologies is an AI-driven tech company specializing in AI systems, agent workflows, and automation.", "general"),
            ("How do I reset my password?", "Go to settings, click security, and choose 'Reset Password'. A link will be sent to your email.", "account"),
            ("What are your business hours?", "Our support operates 24/7 via automated agents and Mon-Fri 9 AM - 6 PM PKT for human specialists.", "support"),
            ("How does billing work?", "We bill monthly based on active automation nodes and compute usage. Invoices are dispatched on the 1st of each month.", "billing")
        ]
        cursor.executemany("INSERT INTO faq_items (question, answer, category) VALUES (?, ?, ?)", seed_faqs)
        conn.commit()
    conn.close()

def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
    conn.commit()
    conn.close()

def get_history(session_id: str, limit: int = 10) -> List[Dict[str, str]]:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?", (session_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

def save_escalation(ticket_id: str, session_id: str, user_id: str, reason: str, urgency: str):
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO escalations (ticket_id, session_id, user_id, reason, urgency) VALUES (?, ?, ?, ?, ?)",
                   (ticket_id, session_id, user_id, reason, urgency))
    conn.commit()
    conn.close()

def search_faqs(query: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    cursor = conn.cursor()
    words = query.lower().split()
    results = []
    cursor.execute("SELECT question, answer, category FROM faq_items")
    for q, a, cat in cursor.fetchall():
        q_lower = q.lower()
        score = sum(1 for w in words if w in q_lower)
        if score > 0:
            results.append({"question": q, "answer": a, "category": cat, "score": score})
    conn.close()
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
