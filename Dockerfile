# ── Single-stage build ──
FROM python:3.12-slim

# Create non-root user
RUN groupadd -r plugin && useradd -r -g plugin plugin

WORKDIR /app

# Install dependencies (system-wide, accessible by all users)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (as package, so python -m app.main works)
COPY app/ ./app/

# Ensure app dir has __init__.py
RUN touch app/__init__.py

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, json; r = urllib.request.urlopen('http://localhost:8080/health'); assert json.loads(r.read())['status'] == 'ok'" || exit 1

USER plugin
ENTRYPOINT ["python", "-m", "app.main"]
