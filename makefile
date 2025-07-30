ruff:
	uv run ruff check . --fix

test:
	uv run -m pytest