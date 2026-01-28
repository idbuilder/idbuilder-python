"""Response types for the IDBuilder SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from snowflake import SnowflakeGenerator

T = TypeVar("T")


@dataclass
class ApiResponse(Generic[T]):
    """Standard API response wrapper."""

    code: int
    message: str
    data: T | None

    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.code == 0


@dataclass
class IncrementIdResponse:
    """Response for increment ID generation."""

    ids: list[int]


@dataclass
class FormattedIdResponse:
    """Response for formatted ID generation."""

    ids: list[str]


@dataclass
class SnowflakeIdResponse:
    """Response for snowflake configuration."""

    worker_id: int
    epoch: int
    worker_bits: int
    sequence_bits: int

    def into_generator(self) -> SnowflakeGenerator:
        """Convert this configuration into a local snowflake generator."""
        from snowflake import SnowflakeGenerator

        return SnowflakeGenerator(
            worker_id=self.worker_id,
            epoch=self.epoch,
            worker_bits=self.worker_bits,
            sequence_bits=self.sequence_bits,
        )
