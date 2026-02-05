---
name: project-methodology
description: High‑level development methodology for AI‑assisted FastAPI + Vue projects.
---

# Project Methodology Skill

This skill encapsulates the overarching philosophy behind this plugin’s workflow.  It is intended to be invoked implicitly when coordinating multi‑agent development.

## Multi‑agent TDD

- **Tests first.**  Each new feature begins with a failing test written by the `@test‑automator`.  Tests act as the specification for the desired behaviour.
- **Minimal implementation.**  The `@coder` writes the minimal code necessary to satisfy the test and nothing more.  Avoid premature optimisation or refactoring.
- **Review and merge.**  The `@reviewer` runs the full test suite in a Docker container, then creates a branch, commits the changes and opens a pull request when all tests pass.  The `@documenter` updates documentation accordingly.

## Database‑aware development

- Always inspect the current schema using `db:list_tables` and `db:get_table_schema` before modifying models.  This aligns code with reality and prevents mismatches.
- Use Alembic migrations to apply schema changes.  Generate migrations via `alembic revision --autogenerate -m "description"` but do not run them manually; tests and deployments will handle applying them.

## Separation of concerns

- Each agent has a single, focused purpose.  This follows the recommended design pattern of granular plugins and minimal token usage.
- Common knowledge and reusable instructions are extracted into Skills.  Skills provide progressive disclosure and are only loaded when needed.

## Code conventions

- **Backend:** Use asynchronous FastAPI endpoints with dependency injection.  SQLAlchemy models should be defined using declarative syntax.  Pydantic schemas validate request and response data.
- **Frontend:** Build components with the Vue 3 Composition API.  Use Pinia for state management and Tailwind CSS classes for styling.  API calls should use relative paths (e.g. `/api/tasks`).
- **Environment configuration:** Use `.env` files and environment variables to configure database credentials, API URLs and other secrets.  Do not commit secrets to version control.

## Development tips

- Regularly run `docker compose -f docker/docker-compose.yaml ps` to check service health and `docker compose -f docker/docker-compose.yaml logs -f` to view logs.  Stop services with `docker compose -f docker/docker-compose.yaml down` when done.
- When debugging, reproduce errors inside Docker to ensure environment consistency.  Avoid running tests directly on your host machine unless you mirror the container setup.
- Document your changes as you go.  Good documentation improves maintainability and helps others understand your design decisions.
