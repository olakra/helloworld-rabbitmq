# RabbitMQ Monorepo — 0→1 Training

A learning-focused monorepo demonstrating a RabbitMQ RPC (request/reply) pattern with services implemented in TypeScript, Go, Python, and Java. The code follows Clean Architecture / DDD patterns and includes TDD-friendly tests.

## What is included
- `services/typescript-service` — full example (server + client), tests (Jest), Dockerfile.
- `services/go-service` — skeleton + example RPC code & tests.
- `services/python-service` — skeleton + example RPC code & tests.
- `services/java-service` — skeleton + example RPC code & tests.
- `docker-compose.yml` — RabbitMQ + sample services
- `pants.toml` — monorepo build tool (Pants)
- `Makefile` — top-level shortcuts
- `.github/workflows/ci.yml` — CI pipeline that runs tests.

## Quickstart (30 minutes)
1. `git clone <this repo>`
2. `docker-compose up --build`
3. Wait for RabbitMQ at http://localhost:15672 (guest/guest)
4. `docker-compose logs -f ts-service` to see example RPC requests/responses.

## Learning objectives
- Understand RabbitMQ RPC pattern (request/reply).
- See cross-language integrations communicating through RabbitMQ.
- Apply TDD, DDD, Clean Architecture patterns in small services.
