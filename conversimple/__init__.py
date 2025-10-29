"""
Conversimple SDK - Python client library for the Conversational AI Platform.

This SDK enables customers to build and deploy AI agents that integrate with
the Conversimple platform's WebRTC infrastructure and conversation management.
"""

from .agent import ConversimpleAgent
from .dispatcher import AgentRegistry, ConversimpleDispatcher, run_dispatcher
from .tools import tool, tool_async
from .callbacks import (
    ConversationLifecycleEvent,
    ToolCallEvent,
    ErrorEvent,
    ConfigUpdateEvent
)
from .api import (
    PlatformClient,
    Agent,
    Deployment,
    ApiKeyInfo,
    ApiKeyUsage,
    ListResponse,
    APIError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from .config import Config

__version__ = "0.3.0"
__all__ = [
    # Configuration
    "Config",
    # Agent execution
    "ConversimpleAgent",
    "tool",
    "tool_async",
    # Event callbacks
    "ConversationLifecycleEvent",
    "ToolCallEvent",
    "ErrorEvent",
    "ConfigUpdateEvent",
    # Dispatcher
    "AgentRegistry",
    "ConversimpleDispatcher",
    "run_dispatcher",
    # Platform API client
    "PlatformClient",
    # API models
    "Agent",
    "Deployment",
    "ApiKeyInfo",
    "ApiKeyUsage",
    "ListResponse",
    # API exceptions
    "APIError",
    "ValidationError",
    "NotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
]
