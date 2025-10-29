"""HTTP client and main PlatformClient for Conversimple API."""

import json
import logging
from typing import Any, Optional

import httpx

from conversimple.api.exceptions import (
    APIError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from conversimple.api.endpoints.agents import AgentEndpoint
from conversimple.api.endpoints.api_keys import ApiKeyEndpoint
from conversimple.api.endpoints.deployments import DeploymentEndpoint
from conversimple.config import Config

logger = logging.getLogger(__name__)


class HTTPClient:
    """Base HTTP client for API requests."""

    def __init__(
        self,
        api_key: str,
        api_endpoint: Optional[str] = None,
        timeout: Optional[int] = None,
        verbose: Optional[bool] = None,
    ):
        """Initialize HTTP client.

        Args:
            api_key: API key for authentication
            api_endpoint: API endpoint URL (defaults from Config)
            timeout: Request timeout in seconds (defaults from Config)
            verbose: Enable verbose logging (defaults from Config)
        """
        self.api_key = api_key
        self.api_endpoint = (api_endpoint or Config.API_ENDPOINT).rstrip("/")
        self.timeout = timeout if timeout is not None else Config.API_TIMEOUT
        self.verbose = verbose if verbose is not None else Config.VERBOSE

        if self.verbose:
            logger.setLevel(logging.DEBUG)

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication.

        Returns:
            Headers dictionary
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "conversimple-sdk/0.3.0",
        }

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle API error responses.

        Args:
            response: HTTP response

        Raises:
            Specific APIError subclass based on status code
        """
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"message": response.text}

        error_message = data.get("message", response.reason_phrase)

        if response.status_code == 422:
            raise ValidationError(
                message=error_message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                message=error_message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 401:
            raise UnauthorizedError(
                message=error_message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 403:
            raise ForbiddenError(
                message=error_message,
                status_code=response.status_code,
                response_data=data,
            )
        else:
            raise APIError(
                message=error_message,
                status_code=response.status_code,
                response_data=data,
            )

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make GET request.

        Args:
            path: API path (e.g., "/api/v1/agents")
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            APIError or subclass for error responses
        """
        url = f"{self.api_endpoint}{path}"
        headers = self._get_headers()

        if self.verbose:
            logger.debug(f"GET {url} params={params}")

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, params=params, headers=headers)

        if response.status_code >= 400:
            self._handle_error(response)

        return response.json()

    def post(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make POST request.

        Args:
            path: API path
            json: Request body as JSON

        Returns:
            Response JSON

        Raises:
            APIError or subclass for error responses
        """
        url = f"{self.api_endpoint}{path}"
        headers = self._get_headers()

        if self.verbose:
            logger.debug(f"POST {url} body={json}")

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=json, headers=headers)

        if response.status_code >= 400:
            self._handle_error(response)

        return response.json()

    def put(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make PUT request.

        Args:
            path: API path
            json: Request body as JSON

        Returns:
            Response JSON

        Raises:
            APIError or subclass for error responses
        """
        url = f"{self.api_endpoint}{path}"
        headers = self._get_headers()

        if self.verbose:
            logger.debug(f"PUT {url} body={json}")

        with httpx.Client(timeout=self.timeout) as client:
            response = client.put(url, json=json, headers=headers)

        if response.status_code >= 400:
            self._handle_error(response)

        return response.json()

    def delete(self, path: str) -> dict[str, Any]:
        """Make DELETE request.

        Args:
            path: API path

        Returns:
            Response JSON

        Raises:
            APIError or subclass for error responses
        """
        url = f"{self.api_endpoint}{path}"
        headers = self._get_headers()

        if self.verbose:
            logger.debug(f"DELETE {url}")

        with httpx.Client(timeout=self.timeout) as client:
            response = client.delete(url, headers=headers)

        if response.status_code >= 400:
            self._handle_error(response)

        return response.json()


class PlatformClient:
    """Conversimple Platform API Client.

    Main entry point for managing agents, deployments, and API keys
    on the Conversimple platform.

    Example:
        ```python
        from conversimple import PlatformClient

        client = PlatformClient(api_key="your-api-key")

        # Agent management
        agents = client.agents.list_agents()
        agent = client.agents.create_agent(
            name="Support Bot",
            description="Customer support agent"
        )

        # Deployment management
        deployment = client.deployments.create_deployment(
            name="Support Widget",
            agent_id=agent.id,
            channel="widget"
        )

        # API key management
        key_info = client.api_keys.get_api_key_info()
        ```
    """

    def __init__(
        self,
        api_key: str,
        api_endpoint: Optional[str] = None,
        timeout: Optional[int] = None,
        verbose: Optional[bool] = None,
    ):
        """Initialize PlatformClient.

        Args:
            api_key: API key for authentication
            api_endpoint: API endpoint URL (defaults from Config)
            timeout: Request timeout in seconds (defaults from Config)
            verbose: Enable verbose logging (defaults from Config)
        """
        self._http_client = HTTPClient(
            api_key=api_key,
            api_endpoint=api_endpoint,
            timeout=timeout,
            verbose=verbose,
        )

        self.agents = AgentEndpoint(self._http_client)
        self.deployments = DeploymentEndpoint(self._http_client)
        self.api_keys = ApiKeyEndpoint(self._http_client)
