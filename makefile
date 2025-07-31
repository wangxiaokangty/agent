.PHONY: lint format

all: lint format

ruff:
	uvx ruff check . --fix

format:
	uvx ruff format .

test:
	uv run -m pytest