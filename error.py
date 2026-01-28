"""Custom exceptions for the IDBuilder SDK."""


class IdBuilderError(Exception):
    """Base exception for all IDBuilder errors."""


class ConfigNotFoundError(IdBuilderError):
    """Configuration key was not found."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"configuration not found: {key}")


class UnauthorizedError(IdBuilderError):
    """Authentication failed - invalid or missing token."""

    def __init__(self, message: str = "unauthorized") -> None:
        super().__init__(message)


class ForbiddenError(IdBuilderError):
    """Token lacks permission for this operation."""

    def __init__(self, message: str = "forbidden") -> None:
        super().__init__(message)


class RateLimitedError(IdBuilderError):
    """Rate limit exceeded."""

    def __init__(self, message: str = "rate limited") -> None:
        super().__init__(message)


class SequenceExhaustedError(IdBuilderError):
    """Sequence has been exhausted for the given key."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"sequence exhausted for key: {key}")


class ClockMovedBackwardsError(IdBuilderError):
    """System clock moved backwards."""

    def __init__(self, message: str = "clock moved backwards") -> None:
        super().__init__(message)


class SequenceOverflowError(IdBuilderError):
    """Snowflake sequence overflow within the same millisecond."""

    def __init__(self, message: str = "sequence overflow") -> None:
        super().__init__(message)


class ApiError(IdBuilderError):
    """API returned an error response."""

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"API error (code={code}): {message}")


class HttpError(IdBuilderError):
    """HTTP transport error."""

    def __init__(self, status_code: int | None, message: str) -> None:
        self.status_code = status_code
        self.message = message
        if status_code:
            super().__init__(f"HTTP error (status={status_code}): {message}")
        else:
            super().__init__(f"HTTP error: {message}")
