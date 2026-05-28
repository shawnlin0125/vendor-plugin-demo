# ── Build Stage ──
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Runtime Stage ──
FROM python:3.12-slim

# Create non-root user
RUN groupadd -r plugin && useradd -r -g plugin plugin

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, json; r = urllib.request.urlopen('http://localhost:8080/health'); assert json.loads(r.read())['status'] == 'ok'" || exit 1

USER plugin
ENTRYPOINT ["python", "main.py"]
