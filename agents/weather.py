from typing import Dict, Any, List
from services.mcp_client import MCPClient

class WeatherAgent:
    @staticmethod
    async def process(destinations: List[str]) -> List[Dict[str, Any]]:
        forecasts = []
        for dest in destinations:
            w = await MCPClient.get_weather(dest)
            forecasts.append(w)
        return forecasts
