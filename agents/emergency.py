from typing import Dict, Any, List
from services.mcp_client import MCPClient

class EmergencyAgent:
    @staticmethod
    async def process(destinations: List[str]) -> Dict[str, Any]:
        return await MCPClient.get_emergency_info(destinations)
