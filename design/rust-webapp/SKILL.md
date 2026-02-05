---
name: rust-webapp
description: Build full-stack web applications using Rust (Axum + SQLx) with HTMX + Alpine.js frontend and Neon (serverless PostgreSQL). Use when asked to create web apps, CRUD apps, dashboards, forms, or any stateful web application. Triggers on requests like "build a todo app", "create a voting app", "make a dashboard", "build a blog", etc.
---

Build full-stack stateful web apps using Axum + HTMX + Alpine.js + Neon (PostgreSQL).

**Stack**: Axum + SQLx (Rust), Askama templates + HTMX + Alpine.js + PicoCSS, Neon (PostgreSQL), Docker.

## Workflow

### Phase 1: Setup

Prerequisites (install once):
```bash
npm i -g neonctl
brew install jq
cargo install sqlx-cli --features postgres,native-tls
```

Required env vars: `NEON_API_KEY`, `NEON_PROJECT_ID`

Scaffold app:
```bash
NEON_BRANCH_TTL=2h .claude/skills/rust-webapp/scripts/scaffold <app-name> .
```

Creates app files and a Neon branch (`{app}-dev`) with 2h expiration.

### Phase 2: Data Modeling

1. Define models in `src/models.rs`
2. Write migration SQL in `migrations/001_init.sql`
3. Use `SERIAL` for i32, `BIGSERIAL` for i64

Reference: [Models](./references/models.md) - SQLx patterns, struct definitions, type mapping

### Phase 3: Backend Implementation

1. Add route handlers in `src/main.rs`
2. All handlers return `Result<T, AppError>` - use `?` operator
3. **NEVER** use `.expect()` or `.unwrap()` - causes server crashes
4. Route params use `{id}` syntax (NOT `:id`)

Reference: [Handlers](./references/handlers.md) - CRUD patterns, router setup, transactions

### Phase 4: Frontend

1. Update Askama templates in `templates/`
2. Delete unused template files (create.html, edit.html if not needed)
3. Use HTMX for interactivity, Alpine.js for state

Reference: [Templates](./references/templates.md) - Askama, HTMX, Alpine patterns
Reference: [Design](./references/design.md) - CSS components, layout patterns

### Phase 5: Validation

Validate (runs cargo check, clippy, tests, release build):
```bash
.claude/skills/rust-webapp/scripts/validate .
```

Fix all errors before completing.

## Template Structure

```
├── Cargo.toml              # Dependencies
├── Dockerfile              # Multi-stage Rust build
├── src/
│   ├── main.rs             # Axum server, routes, templates
│   ├── db.rs               # SQLx pool setup
│   └── models.rs           # Data structs
├── templates/
│   ├── base.html           # Base layout (PicoCSS/HTMX/Alpine CDN)
│   ├── index.html          # List view
│   ├── edit.html           # Edit form
│   └── create.html         # Create form
├── static/
│   └── styles.css          # Custom CSS overrides
└── migrations/
    └── 001_init.sql        # Database schema
```

## Critical Rules

1. **NEVER `.expect()` or `.unwrap()`** in handlers - use `?` operator
2. **Route params: `{id}` not `:id`** - wrong syntax compiles but panics at runtime
3. **All handlers return `Result<T, AppError>`**
4. **Check `rows_affected()`** for DELETE/UPDATE to return 404
5. **Use compile-time SQLx macros** (`query!`, `query_as!`)
6. **Ensure** the app has enough logs for basic observability 

Full list: [Pitfalls](./references/pitfalls.md)

## Constraints

- Neon (PostgreSQL) required - needs `DATABASE_URL`
- All routes at root level (/, /new, /{id}/edit)
- Strict clippy lints - must pass validation
