"""
CatAPI Client — wraps https://thecatapi.com for vendor plugin demo.
"""
import os
import httpx
from typing import Any

CATAPI_BASE = "https://api.thecatapi.com/v1"


async def get_breeds(limit: int = 10) -> list[dict[str, Any]]:
    """Fetch cat breeds from TheCatAPI."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{CATAPI_BASE}/breeds",
            params={"limit": min(limit, 100), "attach_image": 1},
            headers=_headers(),
        )
        resp.raise_for_status()
        return resp.json()


async def search_images(limit: int = 5) -> list[dict[str, Any]]:
    """Search random cat images."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{CATAPI_BASE}/images/search",
            params={
                "limit": min(limit, 50),
                "mime_types": "jpg,png,gif",
                "size": "med",
            },
            headers=_headers(),
        )
        resp.raise_for_status()
        return resp.json()


async def get_breed_by_id(breed_id: str) -> dict[str, Any] | None:
    """Get a specific breed by ID."""
    breeds = await get_breeds(limit=100)
    for breed in breeds:
        if breed.get("id") == breed_id:
            return breed
    return None


def _headers() -> dict[str, str]:
    """Build headers with optional API key."""
    headers = {}
    api_key = os.getenv("CATAPI_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    return headers
