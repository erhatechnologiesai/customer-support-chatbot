# Customer Support Chatbot

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An enterprise-grade, context-aware AI Customer Support Chatbot engineered with FastAPI, SQLite session persistence, real-time sentiment and frustration scoring, and automated human escalation workflows.

---

## Key Features

- **Context-aware**: dialogue maintaining multi-turn conversation memory keyed by session IDs
- **Dynamic**: FAQ retrieval with rapid semantic matching across stored knowledge items
- **Real-time**: sentiment and frustration detection analyzing capitalization, punctuation patterns, and escalation keywords
- **Automated**: human escalation generating high-priority support tickets when customer frustration exceeds thresholds
- **Dual-mode**: execution supporting offline heuristic fallback or live LLM integration

---

## Architecture

```mermaid
flowchart TD
    User([Customer]) -->|HTTP POST /chat| API[FastAPI Server]
    API --> DB[(SQLite Store)]
    API --> Sentiment[Sentiment & Frustration Analyzer]
    Sentiment -->|Score >= Threshold| Escalate[Escalation Service]
    Escalate -->|Create Ticket| Tickets[(Escalation DB)]
    Sentiment -->|Score < Threshold| KB[FAQ & Knowledge Base]
    KB --> LLM[LLM / Heuristic Engine]
    LLM --> API
    API --> User
```

---

## Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Runtime** | Python 3.12 | Core execution environment |
| **API Framework** | FastAPI & Uvicorn | High-performance asynchronous REST endpoints |
| **Data Validation** | Pydantic v2 | Strict schema validation and serialization |
| **Execution Engine** | Dual-Mode (Local + Cloud) | Production-ready logic with offline verification |
| **Testing** | Unittest & Pytest | Deterministic automated verification suite |

---

## Project Structure

```text
customer-support-chatbot/
├── app/
│   ├── __init__.py
│   ├── api.py           # FastAPI routes and server definitions
│   ├── config.py        # Environment variables and application settings
│   ├── models.py        # Pydantic data schemas
│   └── services/        # Core business automation logic
├── tests/
│   ├── __init__.py
│   └── test_chatbot.py   # Automated test suite
├── .env.example         # Template for environment configuration
├── .gitignore           # Python and runtime exclusions
├── LICENSE              # MIT License
├── README.md            # Comprehensive project documentation
└── requirements.txt     # Python package dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (Python 3.12 recommended)
- `pip` package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/erhatechnologiesai/customer-support-chatbot.git
   cd customer-support-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

---

## Running the Application

Start the local development server with auto-reload:

```bash
python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Once running, interactive documentation is accessible at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check and service status |
| `POST` | `/chat` | Process customer message with sentiment tracking and escalation |
| `GET` | `/history/{session_id}` | Retrieve complete conversation transcript for a session |
| `GET` | `/escalations` | List all tickets triggered by safety thresholds |

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"session_id": "cust-01", "message": "I need help with my account"}'
```

---

## Running Tests

Execute the automated test suite:

```bash
python -m unittest tests/test_chatbot.py
```

Or using pytest:

```bash
pytest tests/
```

All test cases are self-contained and run offline without requiring third-party API credentials.

---

## Security & Best Practices

- **Zero Credential Leakage**: API tokens and secrets are loaded exclusively via environment variables and excluded by `.gitignore`.
- **Strict Validation**: All incoming request payloads are strictly validated using Pydantic schemas.
- **Fail-Safe Fallbacks**: Deterministic offline engines guarantee application continuity even during external provider outages.

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).
