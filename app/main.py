"""
Vendor Plugin — FastAPI Application
"""
import os
import time
import logging
from fastapi import FastAPI
from pydantic import BaseModel

# ── Structured JSON logging ──
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
)
logger = logging.getLogger("vendor-plugin")

# ── App ──
app = FastAPI(title=os.getenv("PLUGIN_NAME", "vendor-plugin"), version="0.1.0")

START_TIME = time.time()


@app.get("/health")
async def health():
    """Health check endpoint — required by vendor-contract v1."""
    return {
        "status": "ok",
        "plugin": os.getenv("PLUGIN_NAME", "unknown"),
        "uptime_seconds": int(time.time() - START_TIME),
    }


@app.get("/")
async def root():
    return {"message": f"{os.getenv('PLUGIN_NAME', 'vendor-plugin')} is running"}


# ── Entrypoint ──
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
