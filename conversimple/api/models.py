"""Data models for Conversimple Platform API responses."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ListResponse(BaseModel):
    """Pagination metadata for list responses."""

    page: int
    per_page: int
    total_count: int


class Agent(BaseModel):
    """Agent resource model."""

    id: str
    name: str
    description: str
    status: str  # draft, published, archived
    version: int
    created_at: datetime
    updated_at: datetime
    spec: Optional[dict[str, Any]] = None  # Generated agent specification
    agent_config: Optional[dict[str, Any]] = None  # Agent configuration
    execution_mode: Optional[str] = None  # dialog_manager, free_flow, free_flow_native_sts


class Deployment(BaseModel):
    """Deployment resource model."""

    id: str
    name: str
    agent_id: str
    channel: str  # phone, widget, inline, sdk
    status: str  # pending, active, inactive
    environment: str  # dev, staging, production, widget
    channel_config: Optional[dict[str, Any]] = None
    engagement_rules: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class ApiKeyInfo(BaseModel):
    """API key information."""

    status: str  # active, rotated, expired
    last_4_chars: str = Field(..., alias="last_4")
    created_at: datetime
    last_used_at: Optional[datetime] = None


class ApiKeyUsage(BaseModel):
    """API key usage statistics."""

    requests_24h: int
    requests_month: int
    rate_limit: int
    rate_limit_remaining: int
    last_request_at: Optional[datetime] = None


class AgentListResponse(BaseModel):
    """Response for list agents endpoint."""

    success: bool
    data: list[Agent]
    meta: ListResponse


class AgentResponse(BaseModel):
    """Response for single agent endpoint."""

    success: bool
    data: Agent


class DeploymentListResponse(BaseModel):
    """Response for list deployments endpoint."""

    success: bool
    data: list[Deployment]
    meta: ListResponse


class DeploymentResponse(BaseModel):
    """Response for single deployment endpoint."""

    success: bool
    data: Deployment


class ApiKeyInfoResponse(BaseModel):
    """Response for API key info endpoint."""

    success: bool
    data: ApiKeyInfo


class ApiKeyUsageResponse(BaseModel):
    """Response for API key usage endpoint."""

    success: bool
    data: ApiKeyUsage


class ApiKeyRotateResponse(BaseModel):
    """Response for API key rotate endpoint."""

    success: bool
    data: dict[str, str]  # Contains new_api_key
