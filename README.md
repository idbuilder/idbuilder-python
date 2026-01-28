# IDBuilder Python SDK

Python client library for the IDBuilder distributed ID generation service.

## Features

- **Auto-increment IDs** — Sequential numeric IDs (`1001, 1002, 1003`)
- **Snowflake IDs** — Twitter-style distributed unique IDs (`6982386234567892992`)
- **Formatted IDs** — Human-readable business IDs (`INV20240115-0001`)
- **Thread-safe** — Local snowflake generation is thread-safe
- **Zero dependencies** — Uses only Python standard library

## Requirements

- Python 3.10+

## Installation

```bash
pip install idbuilder
```

## Quick Start

```python
from idbuilder import IdBuilderClient

# Create a client
client = IdBuilderClient("http://localhost:8080", "my-key-token")

# Generate auto-increment IDs
ids = client.increment("order-id").generate(5)
print(ids)  # [1001, 1002, 1003, 1004, 1005]

# Generate a single increment ID
single_id = client.increment("order-id").generate_one()
print(single_id)  # 1006

# Generate formatted IDs
formatted_ids = client.formatted("invoice-id").generate(3)
print(formatted_ids)  # ["INV20240115-0001", "INV20240115-0002", "INV20240115-0003"]
```

## Snowflake ID Generation

Snowflake IDs are generated locally after fetching configuration from the server.
This allows high-throughput ID generation without network calls.

```python
from idbuilder import IdBuilderClient

client = IdBuilderClient("http://localhost:8080", "my-key-token")

# Fetch snowflake configuration (one-time network call)
config = client.snowflake("user-id").get_config()
print(f"Worker ID: {config.worker_id}")
print(f"Epoch: {config.epoch}")

# Create a local generator
generator = config.into_generator()

# Generate IDs locally (no network calls)
id1 = generator.next_id()
ids = generator.next_ids(100)

# Decompose an ID into its components
timestamp, worker_id, sequence = generator.decompose(id1)
print(f"Timestamp: {timestamp}, Worker: {worker_id}, Sequence: {sequence}")
```

## Configuration

```python
from idbuilder import IdBuilderClient, ClientConfig

# Simple initialization
client = IdBuilderClient("http://localhost:8080", "my-key-token")

# With custom timeout
client = IdBuilderClient(
    "http://localhost:8080",
    "my-key-token",
    timeout=60.0,  # 60 seconds
)

# Using ClientConfig
config = ClientConfig(
    base_url="http://localhost:8080",
    key_token="my-key-token",
).with_timeout(60.0)

client = IdBuilderClient.from_config(config)
```

## Error Handling

```python
from idbuilder import (
    IdBuilderClient,
    ConfigNotFoundError,
    UnauthorizedError,
    ForbiddenError,
    RateLimitedError,
    SequenceExhaustedError,
    ClockMovedBackwardsError,
    ApiError,
    HttpError,
)

client = IdBuilderClient("http://localhost:8080", "my-key-token")

try:
    ids = client.increment("order-id").generate(5)
except UnauthorizedError:
    print("Invalid or missing token")
except ForbiddenError:
    print("Token lacks permission")
except ConfigNotFoundError as e:
    print(f"Config not found: {e.key}")
except RateLimitedError:
    print("Rate limit exceeded")
except SequenceExhaustedError as e:
    print(f"Sequence exhausted: {e.key}")
except ApiError as e:
    print(f"API error {e.code}: {e.message}")
except HttpError as e:
    print(f"HTTP error {e.status_code}: {e.message}")
```

## API Reference

### IdBuilderClient

| Method | Returns | Description |
|--------|---------|-------------|
| `increment(key)` | `IncrementApi` | Get increment ID API for key |
| `snowflake(key)` | `SnowflakeApi` | Get snowflake API for key |
| `formatted(key)` | `FormattedApi` | Get formatted ID API for key |

### IncrementApi

| Method | Returns | Description |
|--------|---------|-------------|
| `generate(count=1)` | `list[int]` | Generate multiple IDs (max 1000) |
| `generate_one()` | `int` | Generate single ID |

### SnowflakeApi

| Method | Returns | Description |
|--------|---------|-------------|
| `get_config()` | `SnowflakeIdResponse` | Fetch configuration for local generation |

### FormattedApi

| Method | Returns | Description |
|--------|---------|-------------|
| `generate(count=1)` | `list[str]` | Generate multiple IDs (max 1000) |
| `generate_one()` | `str` | Generate single ID |

### SnowflakeGenerator

| Method | Returns | Description |
|--------|---------|-------------|
| `next_id()` | `int` | Generate single ID (thread-safe) |
| `next_ids(count)` | `list[int]` | Generate multiple IDs |
| `decompose(id)` | `tuple[int, int, int]` | Extract (timestamp, worker_id, sequence) |
| `worker_id` | `int` | Get assigned worker ID |
| `epoch` | `int` | Get custom epoch |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
make test

# Run linting
make lint

# Format code
make fmt

# Type check
make type-check

# Run all checks
make all
```

## License

Apache License 2.0
