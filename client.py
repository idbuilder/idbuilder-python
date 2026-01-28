"""Main client for the IDBuilder SDK."""

from __future__ import annotations

from config import ClientConfig
from api.increment import IncrementApi
from api.snowflake import SnowflakeApi
from api.formatted import FormattedApi


class IdBuilderClient:
    """Client for the IDBuilder distributed ID generation service.

    Example:
        # Simple initialization
        client = IdBuilderClient("http://localhost:8080", "my-key-token")

        # Generate auto-increment IDs
        ids = client.increment("order-id").generate(5)

        # Generate formatted IDs
        ids = client.formatted("invoice-id").generate(3)

        # Get snowflake config and generate IDs locally
        config = client.snowflake("user-id").get_config()
        generator = config.into_generator()
        id = generator.next_id()
    """

    def __init__(
        self,
        base_url: str,
        key_token: str | None = None,
        *,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the client.

        Args:
            base_url: The base URL of the IDBuilder service.
            key_token: The authentication token for API requests.
            timeout: Request timeout in seconds (default: 30).
        """
        self._config = ClientConfig(
            base_url=base_url,
            key_token=key_token,
            timeout=timeout,
        )

    @classmethod
    def from_config(cls, config: ClientConfig) -> IdBuilderClient:
        """Create a client from a configuration object.

        Args:
            config: The client configuration.

        Returns:
            A new IdBuilderClient instance.
        """
        client = cls.__new__(cls)
        client._config = config
        return client

    @property
    def base_url(self) -> str:
        """Get the configured base URL."""
        return self._config.base_url

    @property
    def key_token(self) -> str | None:
        """Get the configured key token."""
        return self._config.key_token

    @property
    def timeout(self) -> float:
        """Get the configured timeout."""
        return self._config.timeout

    def increment(self, key: str) -> IncrementApi:
        """Get the increment ID API for the given key.

        Args:
            key: The configuration key for increment IDs.

        Returns:
            An IncrementApi instance for generating increment IDs.
        """
        return IncrementApi(self, key)

    def snowflake(self, key: str) -> SnowflakeApi:
        """Get the snowflake ID API for the given key.

        Args:
            key: The configuration key for snowflake IDs.

        Returns:
            A SnowflakeApi instance for getting snowflake configuration.
        """
        return SnowflakeApi(self, key)

    def formatted(self, key: str) -> FormattedApi:
        """Get the formatted ID API for the given key.

        Args:
            key: The configuration key for formatted IDs.

        Returns:
            A FormattedApi instance for generating formatted IDs.
        """
        return FormattedApi(self, key)
