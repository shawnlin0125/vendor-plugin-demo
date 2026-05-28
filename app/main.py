"""
Vendor Plugin — FastAPI Application with CatAPI integration.
"""
import os
import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .catapi import get_breeds, search_images, get_breed_by_id

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


# ── Contract Endpoints ──

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
    return {
        "message": f"{os.getenv('PLUGIN_NAME', 'vendor-plugin')} is running",
        "endpoints": {
            "/health": "Health check",
            "/cat/breeds": "List cat breeds (from TheCatAPI)",
            "/cat/breeds/{breed_id}": "Get breed by ID",
            "/cat/images": "Random cat images",
        },
    }


# ── CatAPI Endpoints (Vendor Plugin Demo) ──

@app.get("/cat/breeds")
async def list_breeds(limit: int = 10):
    """Fetch cat breeds from TheCatAPI."""
    try:
        breeds = await get_breeds(limit=limit)
        return {"count": len(breeds), "breeds": breeds}
    except Exception as e:
        logger.error(f"Failed to fetch breeds: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch from external API")


@app.get("/cat/breeds/{breed_id}")
async def breed_detail(breed_id: str):
    """Get details for a specific breed."""
    breed = await get_breed_by_id(breed_id)
    if breed is None:
        raise HTTPException(status_code=404, detail=f"Breed '{breed_id}' not found")
    return breed


@app.get("/cat/images")
async def cat_images(limit: int = 5):
    """Search random cat images."""
    try:
        images = await search_images(limit=limit)
        return {"count": len(images), "images": images}
    except Exception as e:
        logger.error(f"Failed to fetch images: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch from external API")


# ── Entrypoint ──
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
