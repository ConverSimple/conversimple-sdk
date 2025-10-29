"""Configuration management for Conversimple SDK."""

import os
from typing import Optional


class Config:
    """SDK configuration with environment variable support."""

    # API Configuration
    API_ENDPOINT: str = os.getenv(
        "CONVERSIMPLE_API_ENDPOINT",
        "https://api.conversimple.com"
    )
    """Platform API endpoint URL."""

    # Platform WebSocket Configuration
    PLATFORM_URL: str = os.getenv(
        "CONVERSIMPLE_PLATFORM_URL",
        "wss://api.conversimple.com/sdk/websocket"
    )
    """Platform WebSocket URL for agent communication."""

    # Authentication
    API_KEY: Optional[str] = os.getenv("CONVERSIMPLE_API_KEY")
    """API key for authentication (from environment or config file)."""

    CUSTOMER_ID: Optional[str] = os.getenv("CONVERSIMPLE_CUSTOMER_ID")
    """Customer ID (optional, can be derived from API key)."""

    # Logging
    LOG_LEVEL: str = os.getenv("CONVERSIMPLE_LOG_LEVEL", "INFO")
    """Log level for SDK logging."""

    # Client Configuration
    API_TIMEOUT: int = int(os.getenv("CONVERSIMPLE_API_TIMEOUT", "30"))
    """HTTP request timeout in seconds."""

    VERBOSE: bool = os.getenv("CONVERSIMPLE_VERBOSE", "").lower() in ("true", "1", "yes")
    """Enable verbose logging."""

    # Connection Configuration
    HEARTBEAT_INTERVAL: int = int(
        os.getenv("CONVERSIMPLE_HEARTBEAT_INTERVAL", "30")
    )
    """WebSocket heartbeat interval in seconds."""

    MAX_RECONNECT_ATTEMPTS: Optional[int] = None
    """Maximum reconnection attempts (None = infinite)."""

    RECONNECT_BACKOFF: float = float(
        os.getenv("CONVERSIMPLE_RECONNECT_BACKOFF", "2.0")
    )
    """Exponential backoff multiplier for reconnection."""

    MAX_BACKOFF: float = float(
        os.getenv("CONVERSIMPLE_MAX_BACKOFF", "300.0")
    )
    """Maximum backoff time in seconds."""

    TOTAL_RETRY_DURATION: Optional[float] = None
    """Total retry duration limit in seconds (None = no limit)."""

    ENABLE_CIRCUIT_BREAKER: bool = os.getenv(
        "CONVERSIMPLE_ENABLE_CIRCUIT_BREAKER", "true"
    ).lower() in ("true", "1", "yes")
    """Enable circuit breaker for permanent failures."""

    @classmethod
    def update(cls, **kwargs) -> None:
        """Update configuration at runtime.

        Args:
            **kwargs: Configuration key-value pairs
        """
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

    @classmethod
    def get_api_endpoint(cls) -> str:
        """Get API endpoint URL.

        Returns:
            API endpoint URL
        """
        return cls.API_ENDPOINT

    @classmethod
    def get_platform_url(cls) -> str:
        """Get platform WebSocket URL.

        Returns:
            Platform WebSocket URL
        """
        return cls.PLATFORM_URL
