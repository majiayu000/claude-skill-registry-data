---
name: API
description: Reference for the REST API endpoints, request/response formats, and data models. Use when implementing or debugging API-related features.
---

# API Reference

Complete API specification for the Fox English learning service.

## Base URL

- **API Server (Development):** `http://localhost:3001`
- **Frontend (Development):** `http://localhost:3000`
- **API Base Path:** `/api`

## Endpoints

Detailed endpoint specifications are available in the `docs/` directory:

- **[GET /api/articles](docs/get-articles.md)** - Get a list of all articles
- **[GET /api/articles/:id](docs/get-article.md)** - Get a single article by ID

## Architecture

The API follows **Clean Architecture** with these layers:

1. **Domain Layer** - Core business logic (entities, repository interfaces)
2. **Application Layer** - Use cases (business logic orchestration)
3. **Infrastructure Layer** - External dependencies (database, repository implementations)
4. **Presentation Layer** - HTTP interface (controllers, routes, Express app)

**Dependency Rule:** Inner layers never depend on outer layers. Dependencies point inward.

## Key Implementation Details

- **Dependency Injection:** All dependencies manually wired in `api/src/presentation/routes.ts`
- **Repository Pattern:** Domain defines interfaces, infrastructure implements them
- **Database:** MySQL in production, SQLite in-memory for tests
- **Testing:** Integration tests in `api/src/__tests__/integration/`

## Related Skills

- **database** - Database schemas and table specifications
