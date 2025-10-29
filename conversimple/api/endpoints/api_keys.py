"""API key management endpoints."""

from typing import Any

from conversimple.api.models import ApiKeyInfo, ApiKeyUsage


class ApiKeyEndpoint:
    """API key management endpoints."""

    def __init__(self, client: "HTTPClient"):
        """Initialize API key endpoint.

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_api_key_info(self) -> ApiKeyInfo:
        """Get API key information.

        Returns:
            API key information
        """
        response = self.client.get("/api/v1/settings/api-key")
        return ApiKeyInfo(**response["data"])

    def rotate_api_key(self) -> dict[str, str]:
        """Rotate API key.

        Returns:
            Dictionary containing new_api_key
        """
        response = self.client.post("/api/v1/settings/api-key/rotate", json={})
        return response.get("data", {})

    def get_api_key_usage(self) -> ApiKeyUsage:
        """Get API key usage statistics.

        Returns:
            API key usage statistics
        """
        response = self.client.get("/api/v1/settings/api-key/usage")
        return ApiKeyUsage(**response["data"])
