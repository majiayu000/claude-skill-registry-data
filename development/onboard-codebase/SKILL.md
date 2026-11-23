---
name: onboard-codebase
description: >
  Produce a structured, whole-repo orientation guide — entry points,
  architecture layers, conventions, test strategy, and local gotchas — for
  ramping up on a new codebase or context-switching back into one after time
  away. Use when the user says "help me get up to speed on this repo", "give
  me the lay of the land", "onboard me to this codebase", "I'm new here, where
  do I start", or wants a tour of the whole project. Not for a single feature
  or endpoint — use explain-flow instead when the user wants a narrative trace
  of one flow, such as "how login works", rather than orientation to the
  entire repository.
---

# onboard-codebase

You are a codebase orientation guide. Your job is to help a developer understand a repository quickly and accurately — not to produce a generic README summary. Be specific, grounded in actual code, and call out the non-obvious things that trip people up.

---

## Step 1 — Detect project identity

Read the manifest files to establish basic facts:

```
package.json / pyproject.toml / go.mod / Cargo.toml / Gemfile
README.md / README.rst
```

Determine:

- primary language(s)
- framework(s) (Express, NestJS, FastAPI, Django, Rails, Next.js, Echo, Axum, etc.)
- runtime (Node.js version, Python version, Go version)
- package manager (npm, pnpm, yarn, bun, pip, poetry, cargo, etc.)
- whether it is a monorepo or a single-package repo
- the deployment target if visible (container, serverless, edge, traditional server)

---

## Step 2 — Map the directory structure and entry points

Read the top-level directory layout and the primary source directory.

Identify entry points:

- **HTTP server**: file that calls `app.listen()`, `bootstrap()`, `serve()`, or equivalent
- **CLI commands**: main entry files, `bin/` directory, `cmd/` directory
- **Background workers / queues**: job runner files, worker processes, queue consumers
- **Scheduled jobs**: cron definitions, scheduler setup
- **Serverless / Lambda handlers**: handler files, function entry points

For each entry point, note the file path and what it starts.

Map the source directory structure into named layers:

```
src/
  api/            (HTTP layer — controllers, routes, middleware)
  services/       (business logic)
  repositories/   (database access)
  domain/         (entities, value objects, domain events)
  workers/        (background jobs)
  shared/         (utilities, logger, config, errors)
  config/         (environment, app settings)
```

Match the actual structure — do not invent layers that do not exist.

---

## Step 3 — Describe the data model

Find the persistence layer:

- ORM or query builder in use
- schema file location (`prisma/schema.prisma`, `models/`, migration files)
- primary entities and their relationships (read the schema, not just file names)
- database type (PostgreSQL, MySQL, SQLite, MongoDB, Redis, etc.)

Summarize the core domain objects and how they relate. For example:

```
User (1) → (N) Order → (N) OrderItem → (1) Product
```

Do not list every field — only the relationships and key attributes that shape the domain.

---

## Step 4 — Extract conventions

Read 2–3 examples of each of the following and extract the team's actual conventions:

**Code style:**

- where is the lint config? (`eslint.config.*`, `.eslintrc.*`, `pyproject.toml [tool.ruff]`, etc.)
- where is the formatter config? (`.prettierrc`, `pyproject.toml [tool.black]`, `rustfmt.toml`)
- naming patterns: PascalCase classes, camelCase functions, kebab-case files?

**Commit style:**

- check `git log --oneline -10` for the commit message format
- is Conventional Commits enforced? Are there custom prefixes?

**API conventions:**

- URL patterns (REST `/resources/:id`, nested `/users/:id/orders`)
- response envelope shape (`{ data: ..., error: ... }` vs raw)
- error format and status code conventions

**Error handling:**

- does the project use custom error classes? Where are they defined?
- is there a global error handler? Where?

---

## Step 5 — Describe the test strategy

Find the test setup:

- test runner and version (`jest`, `vitest`, `pytest`, `rspec`, `go test`, etc.)
- test file location and naming pattern
- what categories of tests exist: unit, integration, e2e, contract
- what test utilities exist: factories, fixtures, mocks, custom matchers, shared test helpers

Describe how to run a targeted subset of tests locally (the most common daily command).

Identify the test database or mock strategy:

- does integration testing use a real database? How is it set up?
- is there a separate test database config?
- are there Docker dependencies for tests?

---

## Step 6 — Surface common gotchas

This is the most valuable section. Read the README, any `CONTRIBUTING.md`, setup scripts, and recent git history for patterns that suggest non-obvious requirements:

Common gotchas to look for:

- **Environment variable requirements**: which vars must be set before `npm start` works
- **Database setup**: does the dev database need to be seeded? Is there a seed command?
- **Migration requirements**: do migrations need to be run manually after pulling?
- **Service dependencies**: does the app require Redis, a message queue, or an external service to be running locally?
- **Build step requirements**: does TypeScript need to be compiled before running? Is there a codegen step?
- **Port conflicts**: what port does the app run on? Is there a known conflict with another local service?
- **Node/Python/Go version sensitivity**: is a specific version required? Is there an `.nvmrc`, `.python-version`, or `go.mod` pinning a version?
- **Feature flags or config toggles**: are there flags that change app behavior significantly in dev vs prod?

---

## Step 7 — Produce the orientation guide

```text
Codebase orientation: <repo name>
──────────────────────────────────────────────────

Overview
  Language:   <language and version>
  Framework:  <framework>
  Runtime:    <runtime>
  Type:       <monorepo / single package>
  Deploys to: <deployment target if known>

Entry points
  HTTP server:    <file path> — starts on port <N>
  Workers:        <file path> — <what it processes>
  CLI:            <file path> — <how to invoke>

Architecture
  <layer>: <path> — <one-sentence description of what lives here>
  <layer>: <path> — ...

Data model
  <primary entity relationships in plain text>
  ORM: <name>  |  Schema: <path>  |  DB: <type>

Conventions
  Commits:   <format>
  Files:     <naming pattern>
  API:       <URL pattern, response shape>
  Errors:    <custom error classes, global handler location>

Testing
  Runner:    <runner and version>
  Location:  <test file pattern>
  Run all:   <command>
  Run one:   <targeted command example>
  DB:        <real db / mocked / in-memory>

Local setup
  Required env vars: <list the blocking ones>
  Setup steps: <any non-obvious steps beyond npm install>
  Seed data:   <command if applicable>

Gotchas
  1. <most important non-obvious thing>
  2. <next>
  3. ...
──────────────────────────────────────────────────
```
