all: test mypy black

.PHONY: test
test:
	uv run pytest

.PHONY: coverage
coverage:
	uv run pytest --cov src/ofxstatement

.PHONY: black
black:
	uv run black src tests

.PHONY: mypy
mypy:
	uv run mypy src tests
