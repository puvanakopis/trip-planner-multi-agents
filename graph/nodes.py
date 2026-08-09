from typing import Dict, Any
from graph.state import TravelState
from agents.supervisor import SupervisorAgent
from agents.destination import DestinationAgent
from agents.hotel import HotelAgent
from agents.transport import TransportAgent
from agents.activity import ActivityAgent
from agents.weather import WeatherAgent
from agents.emergency import EmergencyAgent
from agents.budget import BudgetAgent
from agents.itinerary import ItineraryAgent
from agents.validator import ValidatorAgent

async def supervisor_node(state: TravelState) -> Dict[str, Any]:
    query = state.get("user_request", "")
    form_data = state.get("travel_request", {})
    req = await SupervisorAgent.process_request(query, form_data)
    return {"travel_request": req}

async def destination_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    res = await DestinationAgent.process(destinations)
    return {"destinations": res}

async def hotel_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    budget = req.get("budget", 150000.0)
    res = await HotelAgent.process(destinations, budget)
    return {"hotels": res}

async def transport_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    origin = req.get("origin", "Colombo")
    destinations = req.get("destinations", [])
    res = await TransportAgent.process(origin, destinations)
    return {"transport": res}

async def activity_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    res = await ActivityAgent.process(destinations)
    return {"activities": res}

async def weather_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    res = await WeatherAgent.process(destinations)
    return {"weather": res}

async def emergency_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    res = await EmergencyAgent.process(destinations)
    return {"emergency": res}

async def budget_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    total_budget = req.get("budget", 150000.0)
    duration_days = req.get("duration_days", 5)
    transport_routes = state.get("transport", [])
    activities = state.get("activities", [])
    res = await BudgetAgent.process(total_budget, transport_routes, activities, duration_days)
    return {"budget": res}

async def itinerary_node(state: TravelState) -> Dict[str, Any]:
    req = state.get("travel_request", {})
    destinations = req.get("destinations", [])
    duration_days = req.get("duration_days", 5)
    origin = req.get("origin", "Colombo")
    activities = state.get("activities", [])
    res = await ItineraryAgent.process(destinations, duration_days, activities, origin)
    return {"itinerary": res}

async def validator_node(state: TravelState) -> Dict[str, Any]:
    res = await ValidatorAgent.process(state)
    return {"validation": res}
