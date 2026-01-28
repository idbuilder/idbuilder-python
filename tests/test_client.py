"""Tests for the IdBuilderClient."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from client import IdBuilderClient
from config import ClientConfig
from api.increment import IncrementApi
from api.snowflake import SnowflakeApi
from api.formatted import FormattedApi


class TestIdBuilderClient:
    """Tests for IdBuilderClient."""

    def test_simple_init(self) -> None:
        """Test simple client initialization."""
        client = IdBuilderClient("http://localhost:8080", "test-token")
        assert client.base_url == "http://localhost:8080"
        assert client.key_token == "test-token"
        assert client.timeout == 30.0

    def test_init_with_timeout(self) -> None:
        """Test client initialization with custom timeout."""
        client = IdBuilderClient(
            "http://localhost:8080",
            "test-token",
            timeout=60.0,
        )
        assert client.timeout == 60.0

    def test_from_config(self) -> None:
        """Test client creation from config."""
        config = ClientConfig(
            base_url="http://localhost:8080",
            key_token="test-token",
            timeout=45.0,
        )
        client = IdBuilderClient.from_config(config)
        assert client.base_url == "http://localhost:8080"
        assert client.key_token == "test-token"
        assert client.timeout == 45.0

    def test_increment_api(self) -> None:
        """Test getting increment API."""
        client = IdBuilderClient("http://localhost:8080", "test-token")
        api = client.increment("order-id")
        assert isinstance(api, IncrementApi)

    def test_snowflake_api(self) -> None:
        """Test getting snowflake API."""
        client = IdBuilderClient("http://localhost:8080", "test-token")
        api = client.snowflake("user-id")
        assert isinstance(api, SnowflakeApi)

    def test_formatted_api(self) -> None:
        """Test getting formatted API."""
        client = IdBuilderClient("http://localhost:8080", "test-token")
        api = client.formatted("invoice-id")
        assert isinstance(api, FormattedApi)


class TestIdBuilderClientEdgeCases:
    """Edge case tests for IdBuilderClient."""

    def test_trailing_slash_removed(self) -> None:
        """Test that trailing slash is removed from base_url."""
        client = IdBuilderClient("http://localhost:8080/", "test-token")
        assert client.base_url == "http://localhost:8080"

    def test_no_token(self) -> None:
        """Test client without token."""
        client = IdBuilderClient("http://localhost:8080")
        assert client.key_token is None

    def test_empty_base_url_raises(self) -> None:
        """Test that empty base_url raises ValueError."""
        with pytest.raises(ValueError, match="base_url is required"):
            IdBuilderClient("", "test-token")
