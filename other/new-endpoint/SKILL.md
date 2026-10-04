---
name: new-endpoint
description: Scaffold a new API endpoint following project conventions. Use when asked to add a new endpoint or resource.
---

Scaffold a complete new endpoint for the resource: $ARGUMENTS

## Step 1 — Understand the project stack and conventions

Before creating anything:
1. Detect the stack: check `package.json`, `pyproject.toml`, `composer.json`, etc.
2. Read 1-2 existing endpoints/routes to understand the project's patterns
3. Identify: where routes live, how validation is done, how errors are handled

**Rule: zero file creation until patterns are understood.**

---

## Step 2 — Scaffold based on stack

### Next.js / Node.js
- Route: `app/api/$ARGUMENTS/route.ts` (Next.js App Router) or `routes/$ARGUMENTS.ts`
- Schema/validation: Zod schema for request body
- Handler: validate input → business logic → return response
- Error handling: try/catch with appropriate HTTP status codes

### Python (FastAPI)
- Schema: `app/schemas/$ARGUMENTS.py` — Create, Update, Response models
- Model: `app/models/$ARGUMENTS.py` — ORM model if needed
- Repository: `app/repositories/$ARGUMENTS.py` — DB operations
- Service: `app/services/$ARGUMENTS.py` — business logic
- Router: `app/routers/$ARGUMENTS.py` — HTTP layer only
- Register in main entry point

### Laravel (PHP)
- Model + migration: `php artisan make:model $ARGUMENTS -m`
- Controller: `php artisan make:controller ${ARGUMENTS}Controller --resource --api`
- Request: `php artisan make:request Store${ARGUMENTS}Request`
- Resource: `php artisan make:resource ${ARGUMENTS}Resource`
- Register routes in `routes/api.php`

---

## Step 3 — Standard endpoints to implement

- `GET /` — list (with pagination if applicable)
- `POST /` — create
- `GET /{id}` — detail
- `PUT /{id}` or `PATCH /{id}` — update
- `DELETE /{id}` — delete

---

## Step 4 — Create tests

Follow the project's existing test patterns. Cover:
- Happy path for each endpoint
- Main error cases (not found, validation failure, unauthorized)

---

## Step 5 — Verify

Run the project's test command (see `run-tests` skill) and confirm the new endpoint works.

$ARGUMENTS
