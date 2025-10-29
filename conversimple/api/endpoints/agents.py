"""Agent management endpoints."""

from typing import Any, Optional

from conversimple.api.models import Agent


class AgentEndpoint:
    """Agent management endpoints."""

    def __init__(self, client: "HTTPClient"):
        """Initialize agent endpoint.

        Args:
            client: HTTP client instance
        """
        self.client = client

    def list_agents(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Agent], dict[str, Any]]:
        """List agents with pagination and filtering.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
            status: Filter by status (draft, published, archived)
            search: Search by name

        Returns:
            Tuple of (agents list, pagination metadata)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        response = self.client.get("/api/v1/agents", params=params)
        agents = [Agent(**agent_data) for agent_data in response["data"]]
        meta = response.get("meta", {})
        return agents, meta

    def create_agent(
        self,
        name: str,
        description: str,
        agent_config: Optional[dict[str, Any]] = None,
    ) -> Agent:
        """Create a new agent.

        Args:
            name: Agent name
            description: Agent description
            agent_config: Optional agent configuration

        Returns:
            Created agent
        """
        payload = {
            "name": name,
            "description": description,
        }
        if agent_config:
            payload["agent_config"] = agent_config

        response = self.client.post("/api/v1/agents", json=payload)
        return Agent(**response["data"])

    def get_agent(self, agent_id: str) -> Agent:
        """Get agent by ID.

        Args:
            agent_id: Agent UUID

        Returns:
            Agent details
        """
        response = self.client.get(f"/api/v1/agents/{agent_id}")
        return Agent(**response["data"])

    def update_agent(
        self,
        agent_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Agent:
        """Update agent.

        Args:
            agent_id: Agent UUID
            name: New agent name
            description: New description
            status: New status (draft, published, archived)

        Returns:
            Updated agent
        """
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if status is not None:
            payload["status"] = status

        if not payload:
            raise ValueError("At least one field must be provided for update")

        response = self.client.put(f"/api/v1/agents/{agent_id}", json=payload)
        return Agent(**response["data"])

    def delete_agent(self, agent_id: str) -> None:
        """Delete agent.

        Args:
            agent_id: Agent UUID
        """
        self.client.delete(f"/api/v1/agents/{agent_id}")

    def get_agent_spec(self, agent_id: str) -> dict[str, Any]:
        """Get agent specification.

        Args:
            agent_id: Agent UUID

        Returns:
            Agent specification (tool definitions, etc.)
        """
        response = self.client.get(f"/api/v1/agents/{agent_id}/spec")
        return response.get("data", {})

    def get_agent_generation_status(self, agent_id: str) -> dict[str, Any]:
        """Get agent generation status.

        Args:
            agent_id: Agent UUID

        Returns:
            Generation status (job_id, status, etc.)
        """
        response = self.client.get(f"/api/v1/agents/{agent_id}/generation-status")
        return response.get("data", {})

    def publish_agent(self, agent_id: str) -> Agent:
        """Publish agent to production.

        Args:
            agent_id: Agent UUID

        Returns:
            Published agent
        """
        response = self.client.post(f"/api/v1/agents/{agent_id}/publish", json={})
        return Agent(**response["data"])
