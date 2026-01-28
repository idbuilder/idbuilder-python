"""Tests for error types."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from error import (
    IdBuilderError,
    ConfigNotFoundError,
    UnauthorizedError,
    ForbiddenError,
    RateLimitedError,
    SequenceExhaustedError,
    ClockMovedBackwardsError,
    SequenceOverflowError,
    ApiError,
    HttpError,
)


class TestErrors:
    """Tests for error types."""

    def test_config_not_found_error(self) -> None:
        """Test ConfigNotFoundError."""
        err = ConfigNotFoundError("test-key")
        assert err.key == "test-key"
        assert "configuration not found: test-key" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_unauthorized_error(self) -> None:
        """Test UnauthorizedError."""
        err = UnauthorizedError()
        assert "unauthorized" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_unauthorized_error_custom_message(self) -> None:
        """Test UnauthorizedError with custom message."""
        err = UnauthorizedError("invalid token")
        assert "invalid token" in str(err)

    def test_forbidden_error(self) -> None:
        """Test ForbiddenError."""
        err = ForbiddenError()
        assert "forbidden" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_rate_limited_error(self) -> None:
        """Test RateLimitedError."""
        err = RateLimitedError()
        assert "rate limited" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_sequence_exhausted_error(self) -> None:
        """Test SequenceExhaustedError."""
        err = SequenceExhaustedError("order-id")
        assert err.key == "order-id"
        assert "sequence exhausted for key: order-id" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_clock_moved_backwards_error(self) -> None:
        """Test ClockMovedBackwardsError."""
        err = ClockMovedBackwardsError()
        assert "clock moved backwards" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_sequence_overflow_error(self) -> None:
        """Test SequenceOverflowError."""
        err = SequenceOverflowError()
        assert "sequence overflow" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_api_error(self) -> None:
        """Test ApiError."""
        err = ApiError(1001, "validation failed")
        assert err.code == 1001
        assert err.message == "validation failed"
        assert "API error (code=1001): validation failed" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_http_error_with_status(self) -> None:
        """Test HttpError with status code."""
        err = HttpError(500, "internal server error")
        assert err.status_code == 500
        assert err.message == "internal server error"
        assert "HTTP error (status=500): internal server error" in str(err)
        assert isinstance(err, IdBuilderError)

    def test_http_error_without_status(self) -> None:
        """Test HttpError without status code."""
        err = HttpError(None, "connection refused")
        assert err.status_code is None
        assert "HTTP error: connection refused" in str(err)


class TestErrorHierarchy:
    """Tests for error inheritance hierarchy."""

    def test_all_errors_inherit_from_base(self) -> None:
        """Test that all errors inherit from IdBuilderError."""
        errors = [
            ConfigNotFoundError("key"),
            UnauthorizedError(),
            ForbiddenError(),
            RateLimitedError(),
            SequenceExhaustedError("key"),
            ClockMovedBackwardsError(),
            SequenceOverflowError(),
            ApiError(1001, "error"),
            HttpError(500, "error"),
        ]
        for err in errors:
            assert isinstance(err, IdBuilderError)
            assert isinstance(err, Exception)
