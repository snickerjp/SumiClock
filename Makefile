.PHONY: help install install-dev format lint type-check test test-cov clean docker-build docker-up docker-down docker-test

help:
	@echo "SumiClock Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format           Format code with black and isort"
	@echo "  make lint             Run flake8 linter"
	@echo "  make type-check       Run mypy type checker"
	@echo "  make check            Run all checks (format, lint, type-check)"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker images"
	@echo "  make docker-up        Start Docker services"
	@echo "  make docker-down      Stop Docker services"
	@echo "  make docker-test      Run tests in Docker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove generated files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pre-commit install

format:
	black --line-length 100 src/ tests/
	isort --profile black --line-length 100 src/ tests/

lint:
	flake8 src/ tests/

type-check:
	mypy src/

check: format lint type-check
	@echo "All checks passed!"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -f test_clock.png
	@echo "Cleanup complete!"
