from pydantic import BaseModel, Field
from typing import Optional, List

class EmergencyFacility(BaseModel):
    name: str
    facility_type: str  # "hospital", "police", "tourist_police", "ambulance"
    destination: str
    contact_number: Optional[str] = None
    address: Optional[str] = None
    distance_km: Optional[float] = None
    source: str = "Overpass API / Sri Lanka Emergency"
    status: str = "verified"

class EmergencyInfo(BaseModel):
    destination: str
    facilities: List[EmergencyFacility] = Field(default_factory=list)
    general_hotlines: dict = Field(default_factory=lambda: {
        "Police Emergency": "119",
        "Ambulance Service (Suwa Seriya)": "1990",
        "Tourist Police": "1912",
        "Fire & Rescue": "110",
        "Government Information Center": "1919"
    })
