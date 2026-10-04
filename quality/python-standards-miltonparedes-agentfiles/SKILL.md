---
name: python-standards
description: Python development standards for personal projects. Use when writing Python code, setting up new projects, configuring tooling, or asking about coding standards. Covers project structure, package management, typing, linting, async patterns, database access, and testing.
---

# Python Standards

## When This Applies

- Starting a new Python project
- Adding dependencies or configuring tooling
- Writing or reviewing Python code
- Unsure about patterns or conventions

## Package Management

- **Must** use `uv` for all projects (Python >= 3.12)
- **Must** define dependencies in `pyproject.toml`
- **Never** use pip directly or requirements.txt for application code
- **Should** pin Python version in `.python-version`

## Core Stack

| Need | Use | Why |
|------|-----|-----|
| Web framework | FastAPI | Async-first, Pydantic integration, OpenAPI |
| Validation / serialization | Pydantic v2 | Performance, native in FastAPI |
| ORM / data layer | SQLModel | Pydantic + SQLAlchemy unified models |
| Database | PostgreSQL | Reliable, feature-rich |
| HTTP client | httpx | Async support, modern API |
| Linting + formatting | ruff | Fast, replaces flake8/isort/black |
| Type checking | ty (astral.sh) | Native uv integration, fast |

## Project Structure

See `references/structure.md` for standard directory layout.

- **Must** separate API, service, and repository layers
- **Must** place external service integrations in `clients/`
- **Should** use `core/` for config, database, exceptions, and logging

## Related Skills

| Topic | Skill |
|-------|-------|
| Typing, linting, exceptions | `/python-code-quality` |
| Async, HTTP, database | `/python-io` |
| Testing patterns | `/python-testing` |
| New project setup | `/python-project-setup` |
