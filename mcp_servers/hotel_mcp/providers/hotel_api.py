import httpx
import os
import datetime
from typing import Dict, Any, List, Optional

class HotelProvider:
    @staticmethod
    async def search_hotels(destination: str, budget: Optional[float] = None) -> Dict[str, Any]:
        """Search hotels using external provider if credentials exist, otherwise return explicit unavailable status."""
        api_key = os.getenv("HOTEL_API_KEY") or os.getenv("RAPIDAPI_KEY")
        
        if not api_key:
            return {
                "destination": destination,
                "hotels": [],
                "source": "External hotel provider",
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "status": "unavailable",
                "message": "Hotel live-search unavailable. (Requires HOTEL_API_KEY in .env)"
            }
        
        # If API key exists, call real hotel provider endpoint (RapidAPI Booking / TripAdvisor API)
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
        params = {"name": f"{destination}, Sri Lanka", "locale": "en-gb"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(url, headers=headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    # Return structured provider results
                    return {
                        "destination": destination,
                        "hotels": data[:5],
                        "source": "Booking.com RapidAPI",
                        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "status": "online",
                        "message": f"Retrieved live hotel listings for {destination}."
                    }
            except Exception as e:
                pass

        return {
            "destination": destination,
            "hotels": [],
            "source": "External hotel provider",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "unavailable",
            "message": "Hotel live-search service currently unavailable or rate limited."
        }
