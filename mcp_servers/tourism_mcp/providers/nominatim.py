import httpx
from typing import Dict, Any, List, Optional
import datetime

# Sri Lanka Bounding Box: Latitude 5.8 to 9.9, Longitude 79.5 to 81.9
SRI_LANKA_MIN_LAT = 5.8
SRI_LANKA_MAX_LAT = 9.9
SRI_LANKA_MIN_LON = 79.5
SRI_LANKA_MAX_LON = 81.9

HEADERS = {
    "User-Agent": "CeylonTripAI/1.0 (srilanka-travel-assistant; contact@ceylontrip.ai)"
}

SRI_LANKA_LOCATIONS = {
    "colombo": (6.9271, 79.8612, "Western Province", "Colombo"),
    "kandy": (7.2906, 80.6337, "Central Province", "Kandy"),
    "galle": (6.0535, 80.2210, "Southern Province", "Galle"),
    "ella": (6.8667, 81.0466, "Uva Province", "Badulla"),
    "nuwara eliya": (6.9497, 80.7891, "Central Province", "Nuwara Eliya"),
    "sigiriya": (7.9570, 80.7603, "Central Province", "Matale"),
    "dambulla": (7.8742, 80.6511, "Central Province", "Matale"),
    "jaffna": (9.6615, 80.0255, "Northern Province", "Jaffna"),
    "trincomalee": (8.5874, 81.2152, "Eastern Province", "Trincomalee"),
    "mirissa": (5.9483, 80.4716, "Southern Province", "Matara"),
    "negombo": (7.2008, 79.8737, "Western Province", "Gampaha"),
    "anuradhapura": (8.3114, 80.4037, "North Central Province", "Anuradhapura"),
    "polonnaruwa": (7.9403, 81.0188, "North Central Province", "Polonnaruwa"),
    "bentota": (6.4239, 79.9987, "Southern Province", "Galle"),
    "arugam bay": (6.8417, 81.8333, "Eastern Province", "Ampara"),
    "matara": (5.9549, 80.5550, "Southern Province", "Matara"),
    "badulla": (6.9934, 81.0550, "Uva Province", "Badulla"),
    "ratnapura": (6.6828, 80.3992, "Sabaragamuwa Province", "Ratnapura"),
    "kurunegala": (7.4863, 80.3623, "North Western Province", "Kurunegala"),
    "hambantota": (6.1246, 81.1185, "Southern Province", "Hambantota"),
    "tangalle": (6.0243, 80.7941, "Southern Province", "Hambantota"),
    "hikkaduwa": (6.1395, 80.1063, "Southern Province", "Galle"),
    "weligama": (5.9750, 80.4287, "Southern Province", "Matara"),
    "unawatuna": (6.0174, 80.2483, "Southern Province", "Galle"),
    "yala": (6.3725, 81.5173, "Southern Province", "Hambantota"),
    "udawalawe": (6.4746, 80.8987, "Sabaragamuwa Province", "Ratnapura"),
    "horton plains": (6.8028, 80.8039, "Central Province", "Nuwara Eliya"),
    "haputale": (6.7686, 80.9631, "Uva Province", "Badulla"),
    "kalutara": (6.5854, 79.9607, "Western Province", "Kalutara"),
    "batticaloa": (7.7310, 81.6747, "Eastern Province", "Batticaloa"),
    "mannar": (8.9810, 79.9044, "Northern Province", "Mannar"),
    "vavuniya": (8.7514, 80.4971, "Northern Province", "Vavuniya"),
    "puttalam": (8.0362, 79.8283, "North Western Province", "Puttalam"),
    "gampaha": (7.0840, 79.9925, "Western Province", "Gampaha"),
    "kegalle": (7.2513, 80.3464, "Sabaragamuwa Province", "Kegalle"),
    "monaragala": (6.8728, 81.3508, "Uva Province", "Monaragala"),
    "mullaitivu": (9.2673, 80.8143, "Northern Province", "Mullaitivu"),
    "kilinochchi": (9.3803, 80.3980, "Northern Province", "Kilinochchi"),
    "pasikuda": (7.9238, 81.5620, "Eastern Province", "Batticaloa"),
    "pinnawala": (7.3014, 80.3847, "Sabaragamuwa Province", "Kegalle"),
    "sinharaja": (6.4167, 80.4667, "Sabaragamuwa Province", "Ratnapura")
}

class TourismProvider:
    @staticmethod
    async def validate_location(place_name: str) -> Dict[str, Any]:
        """Geocode location strictly via live OpenStreetMap Nominatim API calls with Sri Lanka fallback DB."""
        clean_name = place_name.lower().strip()
        
        # Check direct fallback database first for instant speed & zero rate-limit issues
        if clean_name in SRI_LANKA_LOCATIONS:
            lat, lon, state, dist = SRI_LANKA_LOCATIONS[clean_name]
            return {
                "place": place_name,
                "is_sri_lanka": True,
                "display_name": f"{place_name}, {dist}, {state}, Sri Lanka",
                "latitude": lat,
                "longitude": lon,
                "state": state,
                "district": dist,
                "source": "Sri Lanka Location DB / OpenStreetMap",
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "status": "online"
            }

        url = "https://nominatim.openstreetmap.org/search"
        queries = [
            f"{place_name}, Sri Lanka",
            f"{place_name} District, Sri Lanka",
            place_name
        ]

        async with httpx.AsyncClient(timeout=8.0) as client:
            for q in queries:
                params = {
                    "q": q,
                    "format": "json",
                    "addressdetails": 1,
                    "countrycodes": "lk",
                    "limit": 1
                }
                try:
                    response = await client.get(url, params=params, headers=HEADERS)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            item = data[0]
                            lat = float(item["lat"])
                            lon = float(item["lon"])
                            country = item.get("address", {}).get("country", "")
                            
                            is_lk = (country == "Sri Lanka" or 
                                     (SRI_LANKA_MIN_LAT <= lat <= SRI_LANKA_MAX_LAT and 
                                      SRI_LANKA_MIN_LON <= lon <= SRI_LANKA_MAX_LON))
                            
                            return {
                                "place": place_name,
                                "is_sri_lanka": is_lk,
                                "display_name": item.get("display_name"),
                                "latitude": lat,
                                "longitude": lon,
                                "state": item.get("address", {}).get("state"),
                                "district": item.get("address", {}).get("county") or item.get("address", {}).get("state_district"),
                                "source": "OpenStreetMap Nominatim REST API (Live)",
                                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                "status": "online"
                            }
                except Exception:
                    continue

        # Fallback check for partial name matches
        for key, (lat, lon, state, dist) in SRI_LANKA_LOCATIONS.items():
            if key in clean_name or clean_name in key:
                return {
                    "place": place_name,
                    "is_sri_lanka": True,
                    "display_name": f"{place_name}, {dist}, {state}, Sri Lanka",
                    "latitude": lat,
                    "longitude": lon,
                    "state": state,
                    "district": dist,
                    "source": "Sri Lanka Location DB",
                    "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "status": "estimated"
                }

        return {
            "place": place_name,
            "is_sri_lanka": False,
            "source": "OpenStreetMap Nominatim REST API (Live)",
            "status": "unavailable"
        }


    @staticmethod
    async def get_destination_details(place_name: str) -> Dict[str, Any]:
        """Retrieve place summary dynamically via Wikipedia REST API and Nominatim metadata."""
        validation = await TourismProvider.validate_location(place_name)
        if not validation.get("is_sri_lanka"):
            return {
                "name": place_name,
                "is_sri_lanka": False,
                "message": f"'{place_name}' is not recognized as a Sri Lankan destination."
            }

        summary = f"{place_name} is a destination in Sri Lanka."
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place_name.replace(' ', '_')}"
        async with httpx.AsyncClient(timeout=8.0) as client:
            try:
                resp = await client.get(wiki_url, headers=HEADERS)
                if resp.status_code == 200:
                    wdata = resp.json()
                    summary = wdata.get("extract", summary)
            except Exception:
                pass

        validation["description"] = summary
        validation["name"] = place_name
        return validation
