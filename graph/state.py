import operator
from typing import TypedDict, Any, List, Dict, Optional, Annotated

class TravelState(TypedDict, total=False):
    user_request: str
    travel_request: Dict[str, Any]
    destinations: List[Dict[str, Any]]
    hotels: List[Dict[str, Any]]
    transport: List[Dict[str, Any]]
    activities: List[Dict[str, Any]]
    weather: List[Dict[str, Any]]
    emergency: Dict[str, Any]
    budget: Dict[str, Any]
    itinerary: Dict[str, Any]
    required_agents: List[str]
    completed_agents: Annotated[List[str], operator.add]
    agent_workflow: Annotated[List[Dict[str, Any]], operator.add]
    sources: Annotated[List[Dict[str, Any]], operator.add]
    errors: Annotated[List[Dict[str, Any]], operator.add]
    validation: Dict[str, Any]
    final_response: Dict[str, Any]
