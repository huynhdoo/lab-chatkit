# Makefile for ChatKit FastHTML development

.PHONY: help install dev run test lint format clean

help:
	@echo "ChatKit FastHTML - Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make run         - Run production server"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Lint code"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean build artifacts"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

dev:
	python app/main.py

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf dist build *.egg-info
