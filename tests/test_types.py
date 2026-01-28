"""Tests for response types."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    ApiResponse,
    IncrementIdResponse,
    FormattedIdResponse,
    SnowflakeIdResponse,
)
from snowflake import SnowflakeGenerator


class TestApiResponse:
    """Tests for ApiResponse."""

    def test_success_response(self) -> None:
        """Test successful API response."""
        response: ApiResponse[str] = ApiResponse(
            code=0,
            message="success",
            data="test-data",
        )
        assert response.is_success()
        assert response.data == "test-data"

    def test_error_response(self) -> None:
        """Test error API response."""
        response: ApiResponse[str] = ApiResponse(
            code=1001,
            message="validation failed",
            data=None,
        )
        assert not response.is_success()
        assert response.data is None


class TestIncrementIdResponse:
    """Tests for IncrementIdResponse."""

    def test_increment_response(self) -> None:
        """Test IncrementIdResponse."""
        response = IncrementIdResponse(ids=[1001, 1002, 1003])
        assert response.ids == [1001, 1002, 1003]
        assert len(response.ids) == 3


class TestFormattedIdResponse:
    """Tests for FormattedIdResponse."""

    def test_formatted_response(self) -> None:
        """Test FormattedIdResponse."""
        response = FormattedIdResponse(
            ids=["INV-2024-0001", "INV-2024-0002"]
        )
        assert response.ids == ["INV-2024-0001", "INV-2024-0002"]
        assert len(response.ids) == 2


class TestSnowflakeIdResponse:
    """Tests for SnowflakeIdResponse."""

    def test_snowflake_response(self) -> None:
        """Test SnowflakeIdResponse."""
        response = SnowflakeIdResponse(
            worker_id=1,
            epoch=1704067200000,
            worker_bits=10,
            sequence_bits=12,
        )
        assert response.worker_id == 1
        assert response.epoch == 1704067200000
        assert response.worker_bits == 10
        assert response.sequence_bits == 12

    def test_into_generator(self) -> None:
        """Test converting response to generator."""
        response = SnowflakeIdResponse(
            worker_id=5,
            epoch=1704067200000,
            worker_bits=10,
            sequence_bits=12,
        )
        generator = response.into_generator()

        assert isinstance(generator, SnowflakeGenerator)
        assert generator.worker_id == 5
        assert generator.epoch == 1704067200000

    def test_generator_produces_valid_ids(self) -> None:
        """Test that the generator from response produces valid IDs."""
        response = SnowflakeIdResponse(
            worker_id=1,
            epoch=1704067200000,
            worker_bits=10,
            sequence_bits=12,
        )
        generator = response.into_generator()

        ids = generator.next_ids(10)
        assert len(ids) == 10
        assert len(set(ids)) == 10  # All unique

        # Verify worker_id is embedded correctly
        for id_val in ids:
            _, worker_id, _ = generator.decompose(id_val)
            assert worker_id == 1
