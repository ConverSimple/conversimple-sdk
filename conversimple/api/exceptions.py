"""API exceptions for Conversimple Platform Client."""

from typing import Any


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
    ):
        """Initialize APIError.

        Args:
            message: Error message
            status_code: HTTP status code
            response_data: Response data from API
        """
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation."""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class ValidationError(APIError):
    """Raised when API returns 422 Unprocessable Entity (validation errors)."""

    def __init__(
        self,
        message: str = "Validation failed",
        status_code: int = 422,
        response_data: dict[str, Any] | None = None,
    ):
        """Initialize ValidationError."""
        super().__init__(message, status_code, response_data)
        self.errors = response_data.get("errors", {}) if response_data else {}

    def __str__(self) -> str:
        """Return string representation with field errors."""
        base = super().__str__()
        if self.errors:
            errors_str = "\n".join(
                f"  {field}: {error}" for field, error in self.errors.items()
            )
            return f"{base}\n{errors_str}"
        return base


class NotFoundError(APIError):
    """Raised when API returns 404 Not Found."""

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = 404,
        response_data: dict[str, Any] | None = None,
    ):
        """Initialize NotFoundError."""
        super().__init__(message, status_code, response_data)


class UnauthorizedError(APIError):
    """Raised when API returns 401 Unauthorized."""

    def __init__(
        self,
        message: str = "Unauthorized - invalid or missing API key",
        status_code: int = 401,
        response_data: dict[str, Any] | None = None,
    ):
        """Initialize UnauthorizedError."""
        super().__init__(message, status_code, response_data)


class ForbiddenError(APIError):
    """Raised when API returns 403 Forbidden."""

    def __init__(
        self,
        message: str = "Forbidden - you do not have permission to access this resource",
        status_code: int = 403,
        response_data: dict[str, Any] | None = None,
    ):
        """Initialize ForbiddenError."""
        super().__init__(message, status_code, response_data)
