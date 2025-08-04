.PHONY: lint format

all: format lint

lint:
	uvx ruff check . --fix

format:
	uvx ruff format .

test:
	uv run -m pytest

# gui at http://localhost:7474/
neo4j:
	docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$(HOME)/neo4j/data:/data \
	--env=NEO4J_AUTH=none \
	-d \
    neo4j

neo4j-clean:
	rm -r $(HOME)/neo4j/data
