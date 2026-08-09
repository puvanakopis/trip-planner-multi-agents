from typing import Dict, Any, List, Optional
from models.travel import TravelRequest
from config.settings import settings

SRI_LANKA_DISTRICTS_LOWER = [
    "ampara", "anuradhapura", "badulla", "batticaloa", "colombo", 
    "galle", "gampaha", "hambantota", "jaffna", "kalutara", 
    "kandy", "kegalle", "kilinochchi", "kurunegala", "mannar", 
    "matale", "matara", "monaragala", "mullaitivu", "nuwara eliya", 
    "polonnaruwa", "puttalam", "ratnapura", "trincomalee", "vavuniya",
    "ella", "sigiriya", "dambulla", "mirissa", "negombo", "yala", "udawalawe",
    "horton plains", "haputale", "bentota", "arugam bay", "hikkaduwa", "weligama", "unawatuna"
]

class SupervisorAgent:
    @staticmethod
    async def process_request(query: str, form_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyzes query intent, normalizes parameters, and verifies Sri Lanka location scope."""
        data = form_data or {}
        
        origin = data.get("origin", "Colombo")
        destinations = data.get("destinations", [])
        duration_days = data.get("duration_days", 5)
        travelers = data.get("travelers", 2)
        budget = data.get("budget", 150000.0)
        currency = data.get("currency", "LKR")
        travel_style = data.get("travel_style", "Balanced")
        preferences = data.get("preferences", ["Nature", "Culture", "Hiking"])

        if not destinations:
            destinations = ["Badulla", "Nuwara Eliya"]

        # Scope validation for Sri Lanka
        all_places = [origin] + destinations
        is_lk = True
        rejected_places = []
        for p in all_places:
            p_clean = p.strip().lower()
            if not any(district in p_clean or p_clean in district for district in SRI_LANKA_DISTRICTS_LOWER):
                if p_clean not in ["sri lanka", "ceylon"]:
                    is_lk = False
                    rejected_places.append(p)

        if not is_lk:
            return {
                "is_sri_lanka": False,
                "origin": origin,
                "destinations": destinations,
                "rejected_places": rejected_places,
                "message": f"CeylonTrip AI currently supports travel planning exclusively within Sri Lanka. Requested location(s) '{', '.join(rejected_places)}' are outside Sri Lanka."
            }

        return {
            "is_sri_lanka": True,
            "query": query,
            "origin": origin,
            "destinations": destinations,
            "duration_days": duration_days,
            "travelers": travelers,
            "budget": budget,
            "currency": currency,
            "travel_style": travel_style,
            "preferences": preferences,
            "message": "Trip query successfully parsed and validated for Sri Lanka."
        }
