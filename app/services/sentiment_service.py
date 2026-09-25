import re

FRUSTRATION_KEYWORDS = [
    "angry", "furious", "terrible", "worst", "unacceptable", "broken",
    "scam", "useless", "lawyer", "refund", "cancel subscription", "hate",
    "ridiculous", "human", "agent now", "manager", "stolen"
]

def analyze_sentiment(text: str) -> float:
    """
    Returns a sentiment frustration score from 0.0 (calm/positive) to 1.0 (highly frustrated).
    """
    text_lower = text.lower()
    matches = sum(1 for kw in FRUSTRATION_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
    
    # Check exclamation marks and caps
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    exclamations = text.count("!")
    
    score = min(1.0, (matches * 0.25) + (caps_ratio * 0.3) + (min(exclamations, 3) * 0.1))
    return round(score, 2)
