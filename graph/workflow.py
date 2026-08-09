import asyncio
from typing import Dict, Any, Optional
from graph.state import TravelState
from graph import nodes

async def run_travel_plan(query: str, form_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Orchestrates multi-agent execution pipeline for Sri Lanka travel operations."""
    state: TravelState = {
        "user_request": query,
        "travel_request": form_data or {}
    }

    # Step 1: Supervisor Node (Scope & intent parsing)
    sup_res = await nodes.supervisor_node(state)
    state["travel_request"] = sup_res["travel_request"]

    # Rejection check for non-Sri Lanka locations
    if not state["travel_request"].get("is_sri_lanka", True):
        return state

    # Step 2: Parallel execution of specialized data gathering agents
    dest_res, hotel_res, transport_res, act_res, weather_res, emerg_res = await asyncio.gather(
        nodes.destination_node(state),
        nodes.hotel_node(state),
        nodes.transport_node(state),
        nodes.activity_node(state),
        nodes.weather_node(state),
        nodes.emergency_node(state)
    )

    state["destinations"] = dest_res["destinations"]
    state["hotels"] = hotel_res["hotels"]
    state["transport"] = transport_res["transport"]
    state["activities"] = act_res["activities"]
    state["weather"] = weather_res["weather"]
    state["emergency"] = emerg_res["emergency"]

    # Step 3: Sequential execution of synthesis agents (Budget, Itinerary, Validator)
    budget_res = await nodes.budget_node(state)
    state["budget"] = budget_res["budget"]

    itin_res = await nodes.itinerary_node(state)
    state["itinerary"] = itin_res["itinerary"]

    valid_res = await nodes.validator_node(state)
    state["validation"] = valid_res["validation"]

    return state
