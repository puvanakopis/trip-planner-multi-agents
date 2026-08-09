from typing import Dict, Any, List, Optional
from mcp_servers.tourism_mcp.providers.nominatim import TourismProvider
from mcp_servers.hotel_mcp.providers.hotel_api import HotelProvider
from mcp_servers.transport_mcp.providers.osrm import TransportProvider
from mcp_servers.activity_mcp.providers.overpass import ActivityProvider
from mcp_servers.weather_mcp.providers.open_meteo import WeatherProvider
from mcp_servers.emergency_mcp.providers.emergency_provider import EmergencyProvider

class MCPClient:
    @staticmethod
    async def validate_location(location: str) -> Dict[str, Any]:
        return await TourismProvider.validate_location(location)

    @staticmethod
    async def get_destination_details(destination: str) -> Dict[str, Any]:
        return await TourismProvider.get_destination_details(destination)

    @staticmethod
    async def search_hotels(destination: str, budget: Optional[float] = None) -> Dict[str, Any]:
        return await HotelProvider.search_hotels(destination, budget)

    @staticmethod
    async def get_route(origin: str, destination: str) -> Dict[str, Any]:
        return await TransportProvider.get_route(origin, destination)

    @staticmethod
    async def get_activities(destination: str) -> List[Dict[str, Any]]:
        return await ActivityProvider.get_activities(destination)

    @staticmethod
    async def get_weather(destination: str) -> Dict[str, Any]:
        return await WeatherProvider.get_forecast(destination)

    @staticmethod
    async def get_emergency_info(destinations: List[str]) -> Dict[str, Any]:
        return await EmergencyProvider.get_emergency_info(destinations)
