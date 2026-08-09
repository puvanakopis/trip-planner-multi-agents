class CeylonTripException(Exception):
    """Base exception for CeylonTrip AI."""
    pass

class NonSriLankaLocationException(CeylonTripException):
    """Raised when a user requests travel outside Sri Lanka."""
    pass

class MCPToolException(CeylonTripException):
    """Raised when an MCP tool fails or times out."""
    pass

class ProviderUnavailableException(CeylonTripException):
    """Raised when an online API provider is unreachable."""
    pass

class BudgetExceededException(CeylonTripException):
    """Raised when estimated cost exceeds the specified budget."""
    pass
