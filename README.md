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

## Quick Start

### Prerequisites
Make sure you have all the required dependencies installed (see [Dependencies](#dependencies) section below).

### Option 1: Full Docker Setup (Recommended)
```bash
# Clone the repository
git clone <this repo>
cd helloworld-rabbitmq

# Start all services with Docker Compose
make up

# View the TypeScript service logs to see RPC demo
docker-compose logs -f ts-service
```

### Option 2: Development Setup
```bash
# Install dependencies for all services
make install

# Run tests to verify everything works
make test

# Start services
make up
```

### Available Make Commands
The project includes a comprehensive Makefile with convenient shortcuts:

```bash
# Service Management
make up          # Start all services with Docker Compose
make down        # Stop all services
make build       # Build Docker images
make all         # Build + Start services

# Development
make test        # Run all tests (TypeScript, Python, Go, Java)
make lint        # Run all linters
make format      # Auto-format all codebases
make clean       # Clean build artifacts
make install     # Install dependencies across all services

# TypeScript-specific
make test-ts     # Run TypeScript tests
make lint-ts     # Run TypeScript linter
make format-ts   # Format TypeScript code
make install-ts  # Install TypeScript dependencies

# Help
make help        # Show all available commands
```

### Verify Setup
1. **RabbitMQ Management UI**: Visit http://localhost:15672 (guest/guest)
2. **View Service Logs**: `docker-compose logs -f ts-service`
3. **Expected Output**: You should see RPC requests and responses in the logs:
   ```
   ts-service-1  |  [x] Awaiting RPC requests
   ts-service-1  | Sending demo RPC call...
   ts-service-1  | RPC response: {
   ts-service-1  |   id: '7d7cb5da-d037-4bed-ab08-e1a3726f1b1c',
   ts-service-1  |   payload: 'Hello from demo client',
   ts-service-1  |   echoedAt: '2025-09-10T19:58:19.156Z'
   ts-service-1  | }
   ```

## Learning objectives
- Understand RabbitMQ RPC pattern (request/reply).
- See cross-language integrations communicating through RabbitMQ.
- Apply TDD, DDD, Clean Architecture patterns in small services.

## Dependencies

This project requires the following tools to be installed on your system:

### Required Dependencies

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Docker** | 20.10+ | Container runtime for services | [Install Docker](https://docs.docker.com/get-docker/) |
| **Docker Compose** | 2.0+ | Multi-container orchestration | Usually included with Docker Desktop |
| **Make** | 4.0+ | Build automation and shortcuts | Pre-installed on macOS/Linux, [Windows](https://www.gnu.org/software/make/) |
| **Node.js** | 18+ | TypeScript service runtime | [Install Node.js](https://nodejs.org/) |
| **npm** | 8+ | Node package manager | Included with Node.js |

### Optional Dependencies

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Pants** | 2.15+ | Monorepo build tool | [Install Pants](https://www.pantsbuild.org/docs/getting-started/installation) |
| **Python** | 3.9+ | Python service development | [Install Python](https://www.python.org/downloads/) |
| **Go** | 1.19+ | Go service development | [Install Go](https://golang.org/doc/install) |
| **Java** | 17+ | Java service development | [Install Java](https://adoptium.net/) |

### Verification

You can verify your installation by running:

```bash
# Check Docker
docker --version
docker-compose --version

# Check Node.js
node --version
npm --version

# Check Make
make --version

# Check optional tools
pants --version  # if using Pants
python3 --version  # if developing Python services
go version  # if developing Go services
java --version  # if developing Java services
```

### Platform-Specific Notes

- **macOS**: All tools can be installed via [Homebrew](https://brew.sh/): `brew install docker node make`
- **Linux**: Use your distribution's package manager (apt, yum, pacman, etc.)
- **Windows**: Use [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Chocolatey](https://chocolatey.org/), or [WSL2](https://docs.microsoft.com/en-us/windows/wsl/)
