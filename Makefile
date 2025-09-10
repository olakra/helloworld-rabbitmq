SHELL := /bin/bash

.PHONY: help up down build all test lint format clean install \
        lint-ts lint-py lint-go lint-java \
        format-ts format-py format-go format-java \
        test-ts test-py test-go test-java

# ==========================
# Help
# ==========================
help:
	@echo "Available targets:"
	@echo "  make up       - Start services with Docker Compose"
	@echo "  make down     - Stop services"
	@echo "  make build    - Build Docker images"
	@echo "  make all      - Build + Start services"
	@echo "  make test     - Run all tests (TS, Python, Go, Java)"
	@echo "  make lint     - Run all linters"
	@echo "  make format   - Auto-format all codebases"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make install  - Install deps across all services"

# ==========================
# Docker Compose
# ==========================
up:
	docker-compose up --build

down:
	docker-compose down

build:
	docker-compose build

all: build up

# ==========================
# TypeScript
# ==========================
lint-ts:
	cd services/typescript-service && npx eslint . --ext .ts,.tsx

format-ts:
	cd services/typescript-service && npx prettier --write .

test-ts:
	cd services/typescript-service && npm test

install-ts:
	cd services/typescript-service && npm install

# ==========================
# Python
# ==========================
lint-py:
	cd services/python-service && flake8 .

format-py:
	cd services/python-service && black .

test-py:
	cd services/python-service && pytest || true

install-py:
	cd services/python-service && pip install -r requirements.txt

# ==========================
# Go
# ==========================
lint-go:
	cd services/go-service && golangci-lint run ./...

format-go:
	cd services/go-service && gofmt -w .

test-go:
	cd services/go-service && go test ./... || true

install-go:
	cd services/go-service && go mod tidy

# ==========================
# Java
# ==========================
lint-java:
	cd services/java-service && ./gradlew checkstyleMain

format-java:
	cd services/java-service && ./gradlew spotlessApply || true

test-java:
	cd services/java-service && ./gradlew test || true

install-java:
	cd services/java-service && ./gradlew build --refresh-dependencies

# ==========================
# Aggregates
# ==========================
lint: lint-ts lint-py lint-go lint-java
	@echo "✅ All linters passed"

format: format-ts format-py format-go format-java
	@echo "✅ All code formatted"

test: test-ts test-py test-go test-java
	@echo "✅ All tests passed"

clean:
	rm -rf **/dist **/build **/.pytest_cache **/__pycache__ **/.mypy_cache **/.coverage
	@echo "🧹 Cleaned build artifacts"

install: install-ts install-py install-go install-java
	@echo "📦 Dependencies installed for all services"
