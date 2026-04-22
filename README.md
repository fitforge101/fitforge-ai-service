🔗 **Central Documentation:** [https://github.com/fitforge101/fitforge-app-docs](https://github.com/fitforge101/fitforge-app-docs)

# AI Agent Service

## Overview
The `ai-agent-service` powers FitBot, a personalized fitness assistant. It dynamically fetches a user's recent workouts, nutrition, and progress from internal microservices, using that context to ground LangChain/Google GenAI responses.

## Features
*   Authenticated `/chat` endpoint utilizing JWT validation via `auth-service`.
*   Concurrent data aggregation from `workout-service`, `nutrition-service`, and `progress-service` via `httpx`.
*   Grounded LLM responses via LangChain without requiring complex tool-calling loops.

## Tech Stack
*   Python 3.12
*   FastAPI (uvicorn)
*   LangChain (Google GenAI)
*   httpx (Async HTTP Client)

## API Endpoints
*   `POST /chat` - Interactive chat endpoint
*   `GET /health` - Healthcheck

## Example Request/Response

**POST `/chat`**
*Request:*
```json
{
  "message": "Based on my recent logs, how am I doing?"
}
```
*Headers:* `Authorization: Bearer <jwt_token>`

*Response:*
```json
{
  "reply": "You're doing great! You hit your calories yesterday and completed your Deadlift session.",
  "user_id": "64a1b2c3d4e5f67890123456"
}
```

## Setup Instructions
1.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Server:**
    ```bash
    uvicorn main:app --reload --port 5006
    ```

## Environment Variables
*   `GOOGLE_API_KEY` (Required for LLM)
*   `LLM_MODEL` (Required, e.g., `gemini-2.5-flash-lite`)
*   `AUTH_SERVICE_URL` (Default: `http://auth-service:5001`)

## Folder Structure
```text
.
├── Dockerfile
├── requirements.txt
├── main.py
├── agent.py
├── auth.py
└── data_fetcher.py
```

## Deployment
Uses a single-stage `Dockerfile` (Python 3.12-slim) running as a non-root user. Deployed via Kubernetes Helm charts.