"""Deployment management endpoints."""

from typing import Any, Optional

from conversimple.api.models import Deployment


class DeploymentEndpoint:
    """Deployment management endpoints."""

    def __init__(self, client: "HTTPClient"):
        """Initialize deployment endpoint.

        Args:
            client: HTTP client instance
        """
        self.client = client

    def list_deployments(
        self,
        page: int = 1,
        per_page: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> tuple[list[Deployment], dict[str, Any]]:
        """List deployments with pagination and filtering.

        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
            agent_id: Filter by agent ID
            status: Filter by status (pending, active, inactive)
            environment: Filter by environment (dev, staging, production, widget)

        Returns:
            Tuple of (deployments list, pagination metadata)
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if agent_id:
            params["agent_id"] = agent_id
        if status:
            params["status"] = status
        if environment:
            params["environment"] = environment

        response = self.client.get("/api/v1/deployments", params=params)
        deployments = [Deployment(**dep_data) for dep_data in response["data"]]
        meta = response.get("meta", {})
        return deployments, meta

    def create_deployment(
        self,
        name: str,
        agent_id: str,
        channel: str,
        environment: str = "widget",
        channel_config: Optional[dict[str, Any]] = None,
        engagement_rules: Optional[dict[str, Any]] = None,
        call_direction: Optional[str] = None,
    ) -> Deployment:
        """Create a new deployment.

        Args:
            name: Deployment name
            agent_id: Agent ID to deploy
            channel: Channel type (phone, widget, inline, sdk)
            environment: Environment (dev, staging, production, widget)
            channel_config: Channel-specific configuration
            engagement_rules: Engagement rules
            call_direction: Call direction (inbound, outbound)

        Returns:
            Created deployment
        """
        payload = {
            "name": name,
            "agent_id": agent_id,
            "channel": channel,
            "environment": environment,
        }
        if channel_config:
            payload["channel_config"] = channel_config
        if engagement_rules:
            payload["engagement_rules"] = engagement_rules
        if call_direction:
            payload["call_direction"] = call_direction

        response = self.client.post("/api/v1/deployments", json=payload)
        return Deployment(**response["data"])

    def get_deployment(self, deployment_id: str) -> Deployment:
        """Get deployment by ID.

        Args:
            deployment_id: Deployment UUID

        Returns:
            Deployment details
        """
        response = self.client.get(f"/api/v1/deployments/{deployment_id}")
        return Deployment(**response["data"])

    def update_deployment(
        self,
        deployment_id: str,
        name: Optional[str] = None,
        environment: Optional[str] = None,
    ) -> Deployment:
        """Update deployment.

        Args:
            deployment_id: Deployment UUID
            name: New deployment name
            environment: New environment

        Returns:
            Updated deployment
        """
        payload = {}
        if name is not None:
            payload["name"] = name
        if environment is not None:
            payload["environment"] = environment

        if not payload:
            raise ValueError("At least one field must be provided for update")

        response = self.client.put(f"/api/v1/deployments/{deployment_id}", json=payload)
        return Deployment(**response["data"])

    def delete_deployment(self, deployment_id: str) -> None:
        """Delete deployment.

        Args:
            deployment_id: Deployment UUID
        """
        self.client.delete(f"/api/v1/deployments/{deployment_id}")

    def activate_deployment(self, deployment_id: str) -> Deployment:
        """Activate deployment.

        Args:
            deployment_id: Deployment UUID

        Returns:
            Activated deployment
        """
        response = self.client.post(
            f"/api/v1/deployments/{deployment_id}/activate",
            json={},
        )
        return Deployment(**response["data"])

    def deactivate_deployment(self, deployment_id: str) -> Deployment:
        """Deactivate deployment.

        Args:
            deployment_id: Deployment UUID

        Returns:
            Deactivated deployment
        """
        response = self.client.post(
            f"/api/v1/deployments/{deployment_id}/deactivate",
            json={},
        )
        return Deployment(**response["data"])
