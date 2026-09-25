import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "AI Customer Support Chatbot"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "chatbot_data.db")
    FRUSTRATION_THRESHOLD: float = float(os.getenv("FRUSTRATION_THRESHOLD", "0.65"))
    SUPPORT_NOTIFICATION_EMAIL: str = os.getenv("SUPPORT_NOTIFICATION_EMAIL", "support@erhatechnologies.com")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

settings = Settings()
