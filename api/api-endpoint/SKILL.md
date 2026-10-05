---
name: api-endpoint
description: Scaffold a new REST API endpoint with route, validation, service, and tests. Use when asked to add a new API endpoint.
---

# API Endpoint Scaffold

Create a new REST endpoint following our standards.

## Steps

1. Read [route-template.ts](./route-template.ts) for structure
2. Define Zod schema for request/response
3. Create route handler in `backend/src/routes/`
4. Create service method in `backend/src/services/`
5. Add repository method if DB access needed
6. Write integration tests
7. Update OpenAPI spec

Arguments: `$ARGUMENTS` — HTTP method and path, e.g. `POST /users/:id/invite`
