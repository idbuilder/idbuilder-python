"""Thread-safe local Snowflake ID generator."""

import threading
import time

from error import ClockMovedBackwardsError


class SnowflakeGenerator:
    """Thread-safe local Snowflake ID generator.

    Generates unique 64-bit IDs using the Snowflake algorithm.
    The ID is composed of:
    - Timestamp (milliseconds since epoch)
    - Worker ID
    - Sequence number

    This generator is thread-safe and can be used concurrently.
    """

    def __init__(
        self,
        worker_id: int,
        epoch: int,
        worker_bits: int,
        sequence_bits: int,
    ) -> None:
        """Initialize the generator.

        Args:
            worker_id: The unique worker identifier.
            epoch: Custom epoch timestamp in milliseconds.
            worker_bits: Number of bits allocated for worker ID.
            sequence_bits: Number of bits allocated for sequence.
        """
        self._worker_id = worker_id
        self._epoch = epoch
        self._worker_bits = worker_bits
        self._sequence_bits = sequence_bits

        self._sequence = 0
        self._last_timestamp = -1
        self._lock = threading.Lock()

        # Pre-calculate masks and shifts
        self._sequence_mask = (1 << sequence_bits) - 1
        self._worker_shift = sequence_bits
        self._timestamp_shift = sequence_bits + worker_bits

    @property
    def worker_id(self) -> int:
        """Get the assigned worker ID."""
        return self._worker_id

    @property
    def epoch(self) -> int:
        """Get the custom epoch timestamp."""
        return self._epoch

    def next_id(self) -> int:
        """Generate the next unique ID.

        Returns:
            A unique 64-bit integer ID.

        Raises:
            ClockMovedBackwardsError: If the system clock moved backwards.
        """
        with self._lock:
            timestamp = self._current_time_millis()

            if timestamp < self._last_timestamp:
                raise ClockMovedBackwardsError(
                    f"clock moved backwards: {self._last_timestamp - timestamp}ms"
                )

            if timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & self._sequence_mask
                if self._sequence == 0:
                    timestamp = self._wait_next_millis(self._last_timestamp)
            else:
                self._sequence = 0

            self._last_timestamp = timestamp

            return self._compose_id(timestamp, self._worker_id, self._sequence)

    def next_ids(self, count: int) -> list[int]:
        """Generate multiple unique IDs.

        Args:
            count: Number of IDs to generate.

        Returns:
            A list of unique 64-bit integer IDs.

        Raises:
            ClockMovedBackwardsError: If the system clock moved backwards.
            ValueError: If count is less than 1.
        """
        if count < 1:
            raise ValueError("count must be at least 1")
        return [self.next_id() for _ in range(count)]

    def decompose(self, id_value: int) -> tuple[int, int, int]:
        """Decompose an ID into its components.

        Args:
            id_value: The ID to decompose.

        Returns:
            A tuple of (timestamp, worker_id, sequence).
        """
        sequence = id_value & self._sequence_mask
        worker_id = (id_value >> self._worker_shift) & (
            (1 << self._worker_bits) - 1
        )
        timestamp = (id_value >> self._timestamp_shift) + self._epoch
        return timestamp, worker_id, sequence

    def _current_time_millis(self) -> int:
        """Get current time in milliseconds since epoch."""
        return int(time.time() * 1000) - self._epoch

    def _wait_next_millis(self, last_timestamp: int) -> int:
        """Wait until the next millisecond."""
        timestamp = self._current_time_millis()
        while timestamp <= last_timestamp:
            time.sleep(0.001)
            timestamp = self._current_time_millis()
        return timestamp

    def _compose_id(self, timestamp: int, worker_id: int, sequence: int) -> int:
        """Compose an ID from its components."""
        return (
            (timestamp << self._timestamp_shift)
            | (worker_id << self._worker_shift)
            | sequence
        )
