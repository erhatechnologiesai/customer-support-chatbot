import unittest
import os
from fastapi.testclient import TestClient
from app.api import app
from app.database import init_db
from app.services.sentiment_service import analyze_sentiment

class TestCustomerSupportChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DATABASE_PATH"] = "test_chatbot.db"
        os.environ["DEMO_MODE"] = "true"
        init_db()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_chatbot.db"):
            try:
                os.remove("test_chatbot.db")
            except Exception:
                pass

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_sentiment_scoring(self):
        calm_score = analyze_sentiment("Can you tell me how to reset my password please?")
        self.assertLess(calm_score, 0.4)
        
        angry_score = analyze_sentiment("THIS IS UNACCEPTABLE! YOUR PRODUCT IS BROKEN AND A TOTAL SCAM! FIX THIS NOW!")
        self.assertGreaterEqual(angry_score, 0.65)

    def test_faq_flow(self):
        payload = {
            "session_id": "test-session-1",
            "user_id": "user-42",
            "message": "How do I reset my password?"
        }
        response = self.client.post("/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Reset Password", data["reply"])
        self.assertFalse(data["escalated"])

    def test_escalation_flow(self):
        payload = {
            "session_id": "test-session-2",
            "user_id": "user-99",
            "message": "I am furious! Cancel subscription immediately, this is terrible and broken!"
        }
        response = self.client.post("/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["escalated"])
        self.assertIn("priority support ticket", data["reply"].lower())

    def test_conversation_history(self):
        session_id = "test-session-3"
        self.client.post("/chat", json={"session_id": session_id, "message": "Hello"})
        response = self.client.get(f"/history/{session_id}")
        self.assertEqual(response.status_code, 200)
        history = response.json()["messages"]
        self.assertGreaterEqual(len(history), 2)

if __name__ == "__main__":
    unittest.main()
