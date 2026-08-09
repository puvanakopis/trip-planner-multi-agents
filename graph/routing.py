from typing import Dict, Any
from graph.state import TravelState

def route_after_supervisor(state: TravelState) -> str:
    req = state.get("travel_request", {})
    if not req.get("is_sri_lanka", True):
        return "end"
    return "parallel_execution"
