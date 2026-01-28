"""Tests for client configuration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from config import ClientConfig


class TestClientConfig:
    """Tests for ClientConfig."""

    def test_basic_config(self) -> None:
        """Test basic configuration creation."""
        config = ClientConfig(base_url="http://localhost:8080")
        assert config.base_url == "http://localhost:8080"
        assert config.key_token is None
        assert config.timeout == 30.0

    def test_config_with_token(self) -> None:
        """Test configuration with token."""
        config = ClientConfig(
            base_url="http://localhost:8080",
            key_token="test-token",
        )
        assert config.key_token == "test-token"

    def test_config_with_timeout(self) -> None:
        """Test configuration with custom timeout."""
        config = ClientConfig(
            base_url="http://localhost:8080",
            timeout=60.0,
        )
        assert config.timeout == 60.0

    def test_trailing_slash_removed(self) -> None:
        """Test that trailing slash is removed from base_url."""
        config = ClientConfig(base_url="http://localhost:8080/")
        assert config.base_url == "http://localhost:8080"

    def test_empty_base_url_raises(self) -> None:
        """Test that empty base_url raises ValueError."""
        with pytest.raises(ValueError, match="base_url is required"):
            ClientConfig(base_url="")

    def test_with_timeout_chaining(self) -> None:
        """Test with_timeout returns self for chaining."""
        config = ClientConfig(base_url="http://localhost:8080")
        result = config.with_timeout(45.0)
        assert result is config
        assert config.timeout == 45.0

    def test_with_key_token_chaining(self) -> None:
        """Test with_key_token returns self for chaining."""
        config = ClientConfig(base_url="http://localhost:8080")
        result = config.with_key_token("new-token")
        assert result is config
        assert config.key_token == "new-token"
