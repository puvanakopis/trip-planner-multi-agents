from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class RouteSegment(BaseModel):
    origin: str
    destination: str
    distance_km: float
    duration_minutes: float
    mode: str  # "train", "bus", "taxi", "tuk_tuk", "private_driver"
    estimated_cost: float = 0.0
    estimated_cost_lkr: float = 0.0
    currency: str = "LKR"
    mode_costs_lkr: Optional[Dict[str, float]] = None
    cost_range_lkr: Optional[Dict[str, float]] = None
    source: str = "OSRM / Route Estimate"
    status: str = "estimated"
    details: Optional[str] = None

class TransportOptions(BaseModel):
    origin: str
    destination: str
    recommended_mode: str
    recommended_cost_lkr: float = 0.0
    estimated_cost_lkr: float = 0.0
    currency: str = "LKR"
    options: List[RouteSegment] = Field(default_factory=list)

