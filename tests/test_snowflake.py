"""Tests for the Snowflake generator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from snowflake import SnowflakeGenerator
from error import ClockMovedBackwardsError


class TestSnowflakeGenerator:
    """Tests for SnowflakeGenerator."""

    @pytest.fixture
    def generator(self) -> SnowflakeGenerator:
        """Create a standard snowflake generator."""
        return SnowflakeGenerator(
            worker_id=1,
            epoch=1704067200000,  # 2024-01-01 00:00:00 UTC
            worker_bits=10,
            sequence_bits=12,
        )

    def test_properties(self, generator: SnowflakeGenerator) -> None:
        """Test generator properties."""
        assert generator.worker_id == 1
        assert generator.epoch == 1704067200000

    def test_generate_single_id(self, generator: SnowflakeGenerator) -> None:
        """Test generating a single ID."""
        id1 = generator.next_id()
        assert isinstance(id1, int)
        assert id1 > 0

    def test_ids_are_unique(self, generator: SnowflakeGenerator) -> None:
        """Test that generated IDs are unique."""
        ids = [generator.next_id() for _ in range(1000)]
        assert len(ids) == len(set(ids))

    def test_ids_are_monotonic(self, generator: SnowflakeGenerator) -> None:
        """Test that IDs are monotonically increasing."""
        ids = [generator.next_id() for _ in range(1000)]
        for i in range(1, len(ids)):
            assert ids[i] > ids[i - 1]

    def test_next_ids_batch(self, generator: SnowflakeGenerator) -> None:
        """Test batch ID generation."""
        ids = generator.next_ids(100)
        assert len(ids) == 100
        assert len(ids) == len(set(ids))

    def test_next_ids_invalid_count(self, generator: SnowflakeGenerator) -> None:
        """Test that invalid count raises ValueError."""
        with pytest.raises(ValueError, match="count must be at least 1"):
            generator.next_ids(0)

    def test_decompose(self, generator: SnowflakeGenerator) -> None:
        """Test ID decomposition."""
        id1 = generator.next_id()
        timestamp, worker_id, sequence = generator.decompose(id1)

        assert worker_id == generator.worker_id
        assert sequence >= 0
        assert timestamp >= generator.epoch

    def test_thread_safety(self, generator: SnowflakeGenerator) -> None:
        """Test thread-safe ID generation."""
        ids: list[int] = []
        lock = threading.Lock()

        def generate_ids() -> None:
            local_ids = [generator.next_id() for _ in range(1000)]
            with lock:
                ids.extend(local_ids)

        threads = [threading.Thread(target=generate_ids) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(ids) == 4000
        assert len(ids) == len(set(ids)), "IDs should be unique across threads"

    def test_concurrent_generation(self, generator: SnowflakeGenerator) -> None:
        """Test concurrent ID generation with ThreadPoolExecutor."""
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(generator.next_ids, 500) for _ in range(8)]
            all_ids = []
            for future in futures:
                all_ids.extend(future.result())

        assert len(all_ids) == 4000
        assert len(all_ids) == len(set(all_ids))

    def test_decompose_roundtrip(self, generator: SnowflakeGenerator) -> None:
        """Test that decompose extracts correct worker_id."""
        for _ in range(100):
            id1 = generator.next_id()
            _, worker_id, _ = generator.decompose(id1)
            assert worker_id == generator.worker_id


class TestSnowflakeGeneratorEdgeCases:
    """Edge case tests for SnowflakeGenerator."""

    def test_different_worker_ids(self) -> None:
        """Test generators with different worker IDs produce different IDs."""
        gen1 = SnowflakeGenerator(
            worker_id=1,
            epoch=1704067200000,
            worker_bits=10,
            sequence_bits=12,
        )
        gen2 = SnowflakeGenerator(
            worker_id=2,
            epoch=1704067200000,
            worker_bits=10,
            sequence_bits=12,
        )

        ids1 = set(gen1.next_ids(100))
        ids2 = set(gen2.next_ids(100))

        assert len(ids1 & ids2) == 0, "Different workers should produce different IDs"

    def test_worker_id_in_decomposed_id(self) -> None:
        """Test that worker ID is correctly embedded in the ID."""
        for worker_id in [0, 1, 100, 511]:
            gen = SnowflakeGenerator(
                worker_id=worker_id,
                epoch=1704067200000,
                worker_bits=10,
                sequence_bits=12,
            )
            id1 = gen.next_id()
            _, extracted_worker_id, _ = gen.decompose(id1)
            assert extracted_worker_id == worker_id
