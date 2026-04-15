# ─────────────────────────────────────────────────────────────────────────────
# FitForge ai-agent-service — Python 3.12 + FastAPI + LangChain
# Multi-stage not needed here; single-stage is clear and fast enough
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Non-root user for security
RUN addgroup --system fitforge && adduser --system --ingroup fitforge fitbot

WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Switch to non-root
USER fitbot

EXPOSE 5006

# Uvicorn with a single worker (scale via K8s replicas, not threads)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5006"]
