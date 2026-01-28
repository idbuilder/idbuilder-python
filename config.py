"""Client configuration for the IDBuilder SDK."""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_TIMEOUT = 30.0  # seconds


@dataclass
class ClientConfig:
    """Configuration for the IDBuilder client.

    Attributes:
        base_url: The base URL of the IDBuilder service.
        key_token: The authentication token for API requests.
        timeout: Request timeout in seconds (default: 30).
    """

    base_url: str
    key_token: str | None = None
    timeout: float = field(default=DEFAULT_TIMEOUT)

    def __post_init__(self) -> None:
        """Validate and normalize configuration."""
        if not self.base_url:
            raise ValueError("base_url is required")
        self.base_url = self.base_url.rstrip("/")

    def with_timeout(self, timeout: float) -> ClientConfig:
        """Set the request timeout and return self for chaining."""
        self.timeout = timeout
        return self

    def with_key_token(self, token: str) -> ClientConfig:
        """Set the key token and return self for chaining."""
        self.key_token = token
        return self
