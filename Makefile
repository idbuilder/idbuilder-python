.PHONY: build test lint fmt fmt-check type-check clean all

build:
	python -m build

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check .

fmt:
	python -m ruff format .

fmt-check:
	python -m ruff format --check .

type-check:
	python -m mypy .

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

all: fmt-check lint type-check test
