from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

class TravelRequest(BaseModel):
    query: Optional[str] = None
    origin: str = "Colombo"
    destinations: List[str] = Field(default_factory=list)
    duration_days: Optional[int] = None
    travelers: int = 1
    budget: Optional[float] = None
    currency: str = "LKR"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    preferences: List[str] = Field(default_factory=list)
    travel_style: Optional[str] = None  # "Budget", "Balanced", "Luxury"

class CostItem(BaseModel):
    item: str
    cost: float
    currency: str = "LKR"
    source: str
    status: str  # "verified" or "estimated" or "unavailable"

class BudgetBreakdown(BaseModel):
    total_budget: float
    currency: str = "LKR"
    total_estimated_cost: float = 0.0
    total_estimated_cost_lkr: float = 0.0
    remaining_budget: float = 0.0
    exchange_rate_to_lkr: float = 1.0
    is_within_budget: bool = True
    items: List[CostItem] = Field(default_factory=list)
    categories: Dict[str, float] = Field(default_factory=dict)

class TravelPlanResponse(BaseModel):
    success: bool
    is_sri_lanka: bool = True
    message: Optional[str] = None
    request_summary: Dict[str, Any] = Field(default_factory=dict)
    destinations: List[Dict[str, Any]] = Field(default_factory=list)
    hotels: List[Dict[str, Any]] = Field(default_factory=list)
    transport: List[Dict[str, Any]] = Field(default_factory=list)
    activities: List[Dict[str, Any]] = Field(default_factory=list)
    weather: List[Dict[str, Any]] = Field(default_factory=list)
    emergency: Dict[str, Any] = Field(default_factory=dict)
    budget: Dict[str, Any] = Field(default_factory=dict)
    itinerary: Dict[str, Any] = Field(default_factory=dict)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    agent_workflow: List[Dict[str, Any]] = Field(default_factory=list)
