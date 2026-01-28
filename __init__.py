"""IDBuilder Python SDK - Distributed ID generation client."""

from client import IdBuilderClient
from config import ClientConfig
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
from snowflake import SnowflakeGenerator
from models import (
    ApiResponse,
    IncrementIdResponse,
    FormattedIdResponse,
    SnowflakeIdResponse,
)

__version__ = "0.1.0"

__all__ = [
    "IdBuilderClient",
    "ClientConfig",
    "IdBuilderError",
    "ConfigNotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
    "RateLimitedError",
    "SequenceExhaustedError",
    "ClockMovedBackwardsError",
    "SequenceOverflowError",
    "ApiError",
    "HttpError",
    "SnowflakeGenerator",
    "ApiResponse",
    "IncrementIdResponse",
    "FormattedIdResponse",
    "SnowflakeIdResponse",
]
