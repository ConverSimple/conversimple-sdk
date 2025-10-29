"""Tests for Conversimple Platform API Client."""

import json
from datetime import datetime

import pytest
import responses

from conversimple import (
    PlatformClient,
    Agent,
    Deployment,
    ApiKeyInfo,
    ApiKeyUsage,
    APIError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from conversimple.config import Config

# Use Config defaults for all test URLs
BASE_URL = Config.API_ENDPOINT


class TestPlatformClientInitialization:
    """Test PlatformClient initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        client = PlatformClient(api_key="test-key")
        assert client._http_client.api_key == "test-key"
        assert client._http_client.api_endpoint == Config.API_ENDPOINT
        assert client._http_client.timeout == 30

    def test_init_with_custom_endpoint(self):
        """Test initialization with custom endpoint."""
        client = PlatformClient(
            api_key="test-key",
            api_endpoint="https://api.dev.conversimple.com"
        )
        assert client._http_client.api_endpoint == "https://api.dev.conversimple.com"

    def test_init_with_trailing_slash(self):
        """Test that trailing slash is stripped from endpoint."""
        client = PlatformClient(
            api_key="test-key",
            api_endpoint=f"{Config.API_ENDPOINT}/"
        )
        assert client._http_client.api_endpoint == Config.API_ENDPOINT

    def test_endpoints_are_accessible(self):
        """Test that all endpoints are accessible."""
        client = PlatformClient(api_key="test-key")
        assert hasattr(client, "agents")
        assert hasattr(client, "deployments")
        assert hasattr(client, "api_keys")


class TestHTTPClientHeaders:
    """Test HTTP client header management."""

    def test_auth_header_format(self):
        """Test that auth header is properly formatted."""
        client = PlatformClient(api_key="my-secret-key")
        headers = client._http_client._get_headers()
        assert headers["Authorization"] == "Bearer my-secret-key"

    def test_content_type_header(self):
        """Test content type header is set."""
        client = PlatformClient(api_key="test-key")
        headers = client._http_client._get_headers()
        assert headers["Content-Type"] == "application/json"

    def test_user_agent_header(self):
        """Test user agent header includes version."""
        client = PlatformClient(api_key="test-key")
        headers = client._http_client._get_headers()
        assert "conversimple-sdk" in headers["User-Agent"]


class TestExceptionHandling:
    """Test exception handling for different HTTP status codes."""

    @responses.activate
    def test_422_validation_error(self):
        """Test that 422 status raises ValidationError."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents",
            json={
                "message": "Validation failed",
                "errors": {"name": "Name is required"}
            },
            status=422,
        )

        client = PlatformClient(api_key="test-key")

        with pytest.raises(ValidationError) as exc_info:
            client._http_client.get("/api/v1/agents")

        assert exc_info.value.status_code == 422
        assert exc_info.value.errors == {"name": "Name is required"}

    @responses.activate
    def test_404_not_found_error(self):
        """Test that 404 status raises NotFoundError."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents/123",
            json={"message": "Agent not found"},
            status=404,
        )

        client = PlatformClient(api_key="test-key")

        with pytest.raises(NotFoundError) as exc_info:
            client._http_client.get("/api/v1/agents/123")

        assert exc_info.value.status_code == 404

    @responses.activate
    def test_401_unauthorized_error(self):
        """Test that 401 status raises UnauthorizedError."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents",
            json={"message": "Invalid API key"},
            status=401,
        )

        client = PlatformClient(api_key="invalid-key")

        with pytest.raises(UnauthorizedError):
            client._http_client.get("/api/v1/agents")

    @responses.activate
    def test_403_forbidden_error(self):
        """Test that 403 status raises ForbiddenError."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents",
            json={"message": "Forbidden"},
            status=403,
        )

        client = PlatformClient(api_key="test-key")

        with pytest.raises(ForbiddenError):
            client._http_client.get("/api/v1/agents")


class TestAgentEndpoint:
    """Test Agent management endpoints."""

    @responses.activate
    def test_list_agents(self):
        """Test listing agents."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents",
            json={
                "success": True,
                "data": [
                    {
                        "id": "agent-1",
                        "name": "Support Bot",
                        "description": "Support agent",
                        "status": "published",
                        "version": 1,
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "meta": {"page": 1, "per_page": 20, "total_count": 1}
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        agents, meta = client.agents.list_agents(page=1, per_page=20)

        assert len(agents) == 1
        assert agents[0].name == "Support Bot"
        assert meta["total_count"] == 1

    @responses.activate
    def test_create_agent(self):
        """Test creating an agent."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/agents",
            json={
                "success": True,
                "data": {
                    "id": "agent-new",
                    "name": "New Agent",
                    "description": "A new agent",
                    "status": "draft",
                    "version": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        agent = client.agents.create_agent(
            name="New Agent",
            description="A new agent"
        )

        assert agent.id == "agent-new"
        assert agent.name == "New Agent"
        assert agent.status == "draft"

    @responses.activate
    def test_get_agent(self):
        """Test getting a single agent."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/agents/agent-1",
            json={
                "success": True,
                "data": {
                    "id": "agent-1",
                    "name": "Support Bot",
                    "description": "Support agent",
                    "status": "published",
                    "version": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        agent = client.agents.get_agent("agent-1")

        assert agent.id == "agent-1"
        assert agent.name == "Support Bot"

    @responses.activate
    def test_update_agent(self):
        """Test updating an agent."""
        responses.add(
            responses.PUT,
            f"{BASE_URL}/api/v1/agents/agent-1",
            json={
                "success": True,
                "data": {
                    "id": "agent-1",
                    "name": "Updated Bot",
                    "description": "Support agent",
                    "status": "draft",
                    "version": 2,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        agent = client.agents.update_agent("agent-1", name="Updated Bot")

        assert agent.name == "Updated Bot"
        assert agent.version == 2

    @responses.activate
    def test_delete_agent(self):
        """Test deleting an agent."""
        responses.add(
            responses.DELETE,
            f"{BASE_URL}/api/v1/agents/agent-1",
            json={"success": True},
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        client.agents.delete_agent("agent-1")

        assert len(responses.calls) == 1

    @responses.activate
    def test_publish_agent(self):
        """Test publishing an agent."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/agents/agent-1/publish",
            json={
                "success": True,
                "data": {
                    "id": "agent-1",
                    "name": "Support Bot",
                    "description": "Support agent",
                    "status": "published",
                    "version": 2,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        agent = client.agents.publish_agent("agent-1")

        assert agent.status == "published"


class TestDeploymentEndpoint:
    """Test Deployment management endpoints."""

    @responses.activate
    def test_list_deployments(self):
        """Test listing deployments."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/deployments",
            json={
                "success": True,
                "data": [
                    {
                        "id": "deploy-1",
                        "name": "Support Widget",
                        "agent_id": "agent-1",
                        "channel": "widget",
                        "status": "active",
                        "environment": "widget",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "meta": {"page": 1, "per_page": 20, "total_count": 1}
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        deployments, meta = client.deployments.list_deployments()

        assert len(deployments) == 1
        assert deployments[0].name == "Support Widget"

    @responses.activate
    def test_create_deployment(self):
        """Test creating a deployment."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/deployments",
            json={
                "success": True,
                "data": {
                    "id": "deploy-new",
                    "name": "Support Widget",
                    "agent_id": "agent-1",
                    "channel": "widget",
                    "status": "pending",
                    "environment": "widget",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        deployment = client.deployments.create_deployment(
            name="Support Widget",
            agent_id="agent-1",
            channel="widget"
        )

        assert deployment.id == "deploy-new"
        assert deployment.channel == "widget"

    @responses.activate
    def test_activate_deployment(self):
        """Test activating a deployment."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/deployments/deploy-1/activate",
            json={
                "success": True,
                "data": {
                    "id": "deploy-1",
                    "name": "Support Widget",
                    "agent_id": "agent-1",
                    "channel": "widget",
                    "status": "active",
                    "environment": "widget",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        deployment = client.deployments.activate_deployment("deploy-1")

        assert deployment.status == "active"


class TestApiKeyEndpoint:
    """Test API Key management endpoints."""

    @responses.activate
    def test_get_api_key_info(self):
        """Test getting API key info."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/settings/api-key",
            json={
                "success": True,
                "data": {
                    "status": "active",
                    "last_4": "1234",
                    "created_at": "2024-01-01T00:00:00Z",
                    "last_used_at": "2024-01-02T00:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        key_info = client.api_keys.get_api_key_info()

        assert key_info.status == "active"
        assert key_info.last_4_chars == "1234"

    @responses.activate
    def test_get_api_key_usage(self):
        """Test getting API key usage statistics."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/settings/api-key/usage",
            json={
                "success": True,
                "data": {
                    "requests_24h": 100,
                    "requests_month": 5000,
                    "rate_limit": 10000,
                    "rate_limit_remaining": 5000,
                    "last_request_at": "2024-01-02T12:00:00Z",
                }
            },
            status=200,
        )

        client = PlatformClient(api_key="test-key")
        usage = client.api_keys.get_api_key_usage()

        assert usage.requests_24h == 100
        assert usage.rate_limit == 10000
