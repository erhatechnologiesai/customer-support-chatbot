import os
from typing import List, Dict, Tuple
from app.config import settings
from app.database import search_faqs

def generate_ai_reply(message: str, history: List[Dict[str, str]]) -> Tuple[str, List[str]]:
    """
    Generates intelligent response using local/mock reasoning engine or OpenAI if configured.
    """
    faqs = search_faqs(message)
    sources = []
    
    if faqs:
        best_faq = faqs[0]
        sources.append(f"FAQ: {best_faq['question']}")
        context_answer = best_faq["answer"]
    else:
        context_answer = None

    if settings.OPENAI_API_KEY and not settings.DEMO_MODE:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            system_prompt = (
                "You are an empathetic, expert customer support AI for Erha Technologies. "
                "Answer user questions accurately and concisely."
            )
            if context_answer:
                system_prompt += f"\nRelevant Knowledge: {context_answer}"
                
            messages = [{"role": "system", "content": system_prompt}]
            for h in history[-4:]:
                messages.append({"role": h["role"], "content": h["content"]})
            messages.append({"role": "user", "content": message})
            
            completion = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=250,
                temperature=0.3
            )
            return completion.choices[0].message.content.strip(), sources
        except Exception as e:
            print(f"[LLM FALLBACK] Failed to call external LLM API ({e}). Falling back to local heuristic.")

    # Intelligent Local Mock / Heuristic Engine
    if context_answer:
        return f"{context_answer} Please let me know if you need further clarification!", sources
        
    m_lower = message.lower()
    if any(g in m_lower for g in ["hi", "hello", "hey", "salam"]):
        return "Hello! Welcome to Erha Technologies Customer Support. How may I assist you today?", sources
    elif "price" in m_lower or "cost" in m_lower or "quote" in m_lower:
        return "Our pricing is tailored to your workload requirements and automation scale. Would you like to schedule an exploratory consultation?", ["Pricing Guidelines"]
    elif "contact" in m_lower or "reach" in m_lower:
        return f"You can reach our human support team directly at {settings.SUPPORT_NOTIFICATION_EMAIL}.", ["Contact Directory"]
    else:
        return "Thank you for reaching out. I've noted your inquiry regarding our AI systems and our team is happy to help. Could you provide a bit more detail?", []
