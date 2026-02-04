---
name: modern-python
description: Modern Python development with uv, FastAPI, Pydantic, and clean architecture. Use for Python project setup, LLM app development, API design, testing strategy, and architecture decisions. Ideal for TypeScript developers transitioning to Python.
---

# Modern Python Development

## Overview

This skill provides modern Python development guidance for 2025, specializing in:
- **LLM Applications**: Structured outputs with Pydantic/Instructor
- **API Development**: FastAPI with type safety and dependency injection
- **Clean Architecture**: Thin, pragmatic application of hexagonal patterns
- **Modern Tooling**: uv, Ruff, mypy, pytest-watch

Designed for TypeScript developers who value simplicity and type safety.

## Core Philosophy

Apply these principles to all Python development:

1. **KISS (Keep It Simple)**: Simple is better than complex
2. **YAGNI (You Aren't Gonna Need It)**: Implement only what's needed now
3. **Boy Scout Rule**: Leave code cleaner than you found it
4. **Reader-Friendly Code**: The next engineer should understand immediately

## When to Use This Skill

Claude should automatically use this skill when:
- Setting up new Python projects
- Designing architecture for LLM applications
- Making decisions about project structure
- Choosing between architectural patterns
- Configuring development tooling (uv, Ruff, mypy)
- Implementing FastAPI endpoints
- Structuring tests (unit/integration/functional)
- Advising TypeScript developers on Python equivalents

## Architecture Decision Framework

### Step 1: Assess Complexity

Choose structure based on project complexity:

| Complexity | Structure | When to Use |
|------------|-----------|-------------|
| **Script/PoC** | Flat (single file) | Quick experiments, one-off scripts |
| **Small App** | 2-layer (domain + adapters) | MVPs, simple APIs |
| **Production** | 3-layer (domain + ports + adapters) | Multiple integrations, complex business logic |

### Step 2: Apply Thin Clean Architecture

**Only add layers when complexity warrants it.**

```
domain/     → Pure business logic (Pydantic models, services)
ports/      → Interfaces (Protocol classes) - add when needed
adapters/   → External integrations (API, DB, LLM clients)
```

**Key principle**: Start simple, refactor when pain points emerge.

### Step 3: Choose Project Structure

- **Single Package**: Use for most projects (PoC, small-medium apps)
- **Monorepo (uv workspaces)**: Use when sharing code across multiple services

See [REFERENCE.md](REFERENCE.md#project-structure) for detailed structures.

## Development Workflow

### Initial Setup

```bash
# 1. Initialize project
uv init my-project && cd my-project

# 2. Add dependencies
uv add fastapi pydantic uvicorn
uv add --dev pytest pytest-watch ruff mypy

# 3. Configure tools
# See REFERENCE.md for pyproject.toml configs
```

### TDD Workflow

```bash
# Terminal 1: Watch tests (auto-run on changes)
uv run ptw -- tests/unit -v

# Terminal 2: Write code
# Follow Red -> Green -> Refactor cycle
```

### Quality Checks

```bash
uv run ruff check --fix .  # Lint & auto-fix
uv run mypy src/           # Type check
uv run pytest --cov=src    # Test with coverage
```

## LLM Application Patterns

### Type-Safe Structured Outputs

**Always use Pydantic for LLM outputs** to ensure type safety:

```python
from pydantic import BaseModel, Field

class ExtractedInfo(BaseModel):
    summary: str = Field(description="Brief summary")
    key_points: list[str]
    sentiment: Literal["positive", "neutral", "negative"]
```

**Use Instructor for type-safe LLM calls**:
```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())
response = client.chat.completions.create(
    model="gpt-4o",
    response_model=ExtractedInfo,
    messages=[{"role": "user", "content": text}]
)
# response is typed as ExtractedInfo ✓
```

See [EXAMPLES.md](EXAMPLES.md#llm-patterns) for more patterns.

## FastAPI Best Practices

### Dependency Injection Pattern

```python
from fastapi import FastAPI, Depends

def get_service() -> UserService:
    # Initialize dependencies here
    return UserService(repo=get_repo())

@app.post("/users")
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_service)
):
    return service.create(request)
```

See [EXAMPLES.md](EXAMPLES.md#fastapi-patterns) for complete examples.

## Testing Strategy

### 3-Layer Test Structure

```
tests/
├── unit/          # Fast, isolated, no I/O
├── integration/   # With real dependencies (DB, cache)
└── functional/    # E2E API tests
```

**Coverage targets**:
- Unit: 80%+ (business logic)
- Integration: Key flows only
- Functional: Critical user journeys

See [EXAMPLES.md](EXAMPLES.md#testing-examples) for test code.

## Do's and Don'ts

### ✅ Do

- Use type hints everywhere (`-> None`, `list[str]`, `dict[str, Any]`)
- Prefer `Protocol` over `ABC` for interfaces
- Use `pydantic.BaseModel` for data classes with validation
- Run `ruff check --fix` before commits
- Keep functions small and focused

### ❌ Don't

- Over-engineer with unnecessary abstraction layers
- Use `Any` type unless absolutely necessary
- Skip type hints "for now"
- Create classes when functions suffice
- Add dependencies without clear need

## TypeScript Developer Quick Reference

| TypeScript | Python Equivalent |
|------------|-------------------|
| `interface` | `Protocol` or `BaseModel` |
| `type` | `TypeAlias` or `Literal` |
| `zod` | `pydantic` |
| `npm/pnpm/yarn` | `uv` |
| `eslint + prettier` | `ruff` |
| `jest/vitest` | `pytest` |
| `express/fastify` | `fastapi` |
| `NestJS DI` | `FastAPI Depends` |

See [EXAMPLES.md](EXAMPLES.md#typescript-python-mapping) for detailed mapping.

## Output Guidelines

When providing guidance:

1. **Explain the "why"** - Rationale behind recommendations
2. **Show concrete examples** - Runnable code snippets
3. **Suggest next steps** - What to implement/consider next
4. **Flag complexity decisions** - When to add vs skip abstraction

**Always prioritize working code over perfect architecture.**

## References

- [REFERENCE.md](REFERENCE.md) - Tool configurations, project structures, commands
- [EXAMPLES.md](EXAMPLES.md) - Code examples, patterns, TypeScript mapping

## Checklist for New Projects

- [ ] Project initialized with `uv init`
- [ ] Dependencies added via `uv add`
- [ ] `pyproject.toml` configured (Ruff, mypy, pytest)
- [ ] Project structure matches complexity level
- [ ] Type hints added to all functions
- [ ] Tests written (at least unit tests)
- [ ] TDD workflow established (`pytest-watch`)
- [ ] Pre-commit hooks considered (optional)
