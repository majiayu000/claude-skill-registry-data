---
name: backend-go
description: Expertise in developing and maintaining the Go backend with Clean Architecture.
---

# Backend (Go) Development Skill

## Main Instructions

When working on the Go backend (`apps/backend/`), you MUST follow these instructions:

### 1. Before Writing Any Code
- Read `docs/clean-architecture.md` to understand the layered architecture.
- Identify which layer(s) the change belongs to:
  - **Entities** (`internal/entity/`): Core domain structs, no external dependencies.
  - **Services** (`internal/service/`): Business logic, defines repository interfaces.
  - **Delivery** (`internal/delivery/http/`): HTTP handlers, request parsing, response formatting.
  - **Middleware** (`internal/middleware/`): Cross-cutting concerns (auth, CORS, logging).
  - **Repository** (`internal/repository/postgres/`): SQL queries, implements service interfaces.

### 2. Dependency Rule (NEVER Violate)
- Dependencies MUST only point inwards: `Delivery -> Service -> Entity`.
- `Repository` implements interfaces defined in `Service`.
- Inner layers (Entity, Service) must NEVER import outer layers (Delivery, Repository).

### 3. When Adding a New Endpoint
1. Define the Entity/Request/Response structs in `internal/entity/`.
2. Add the method signature to the Service interface in `internal/service/`.
3. Implement the business logic in the Service.
4. Add any necessary Repository interface methods and their PostgreSQL implementations.
5. Create the HTTP Handler in `internal/delivery/http/` and register the route.
6. Add or update the OpenAPI spec in `apps/backend/openapi.yaml`.

### 4. When Modifying Existing Code
1. Check which layer the change belongs to.
2. Ensure changes do not introduce cross-layer dependencies that violate the dependency rule.
3. Update related tests.

### 5. Coding Standards
- Use idiomatic Go error handling (`if err != nil`). Wrap errors with context.
- Ensure all public entity structs have proper `json` tags.
- Use `.env` for local configuration; NEVER hardcode secrets or commit `.env`.
- Write unit tests for Services using Mock Repositories.

### 6. Database Changes
- Place migration SQL files in `migrations/` (use naming: `NNN_description.up.sql` / `.down.sql`).
- Place seed data in `seed/`.
- Apply with `make db-migrate`, seed with `make db-seed`, or full reset with `make db-reset`.

### 7. Running & Testing
- Start the server: `make backend-run` (from root) or `go run cmd/main.go` (from `apps/backend`).
- Run tests: `make backend-test` or `go test ./...` from `apps/backend`.

## Reference Examples
- [examples/endpoint_reference.md](examples/endpoint_reference.md): Full end-to-end guide for adding a new endpoint (Entity → Service → Repo → Handler → Route), based on the actual Task implementation.
