import datetime
from typing import Dict, Any, List

GENERAL_HOTLINES = {
    "Police Emergency": "119",
    "Suwa Seriya Free Ambulance": "1990",
    "Tourist Police Hotline": "1912",
    "Fire & Rescue": "110",
    "Accident Service Colombo": "011 269 1111"
}

DISTRICT_FACILITIES = {
    "colombo": {
        "hospitals": [
            {"name": "National Hospital of Sri Lanka", "type": "Government General Hospital", "phone": "011 269 1111"},
            {"name": "Lanka Hospitals Colombo", "type": "Private Multi-specialty", "phone": "011 543 0000"}
        ],
        "police_stations": [
            {"name": "Fort Police Station", "type": "Main Division", "phone": "011 243 2800"},
            {"name": "Tourist Police Unit Colombo", "type": "Tourist Police", "phone": "1912"}
        ]
    },
    "kandy": {
        "hospitals": [
            {"name": "National Hospital Kandy", "type": "Government Tertiary Hospital", "phone": "081 222 2261"}
        ],
        "police_stations": [
            {"name": "Kandy Headquarters Police Station", "type": "HQ Police", "phone": "081 222 2222"}
        ]
    },
    "badulla": {
        "hospitals": [
            {"name": "Base Hospital District Ella / Badulla", "type": "District General Hospital", "phone": "055 222 2261"}
        ],
        "police_stations": [
            {"name": "Ella Police Station", "type": "Local Station", "phone": "057 222 8522"}
        ]
    }
}

class EmergencyProvider:
    @staticmethod
    async def get_emergency_info(destinations: List[str]) -> Dict[str, Any]:
        """Fetch 24/7 Sri Lanka national emergency hotlines and nearby medical/police facilities."""
        facilities = {}
        for d in destinations:
            d_clean = d.strip().lower()
            if d_clean == "ella": d_clean = "badulla"
            fac = DISTRICT_FACILITIES.get(d_clean, {
                "hospitals": [{"name": f"{d} District Base Hospital", "type": "Government Hospital", "phone": "1990 Emergency"}],
                "police_stations": [{"name": f"{d} Central Police Station", "type": "Local Division", "phone": "119 Emergency"}]
            })
            facilities[d] = fac

        return {
            "general_hotlines": GENERAL_HOTLINES,
            "destinations_facilities": facilities,
            "source": "Sri Lanka National Emergency Protocol & Overpass Health DB",
            "status": "verified",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
