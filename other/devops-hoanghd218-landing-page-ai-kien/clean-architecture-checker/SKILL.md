---
name: clean-architecture-checker
description: Verifies code follows Clean Architecture principles in Polibase. Activates when creating or modifying src/domain, src/application, src/infrastructure, or src/interfaces files. Checks dependency rules, entity independence, repository patterns, DTO usage, and type safety.
---

# Clean Architecture Checker

## Purpose
Verify that new code follows Clean Architecture principles as defined in the Polibase project.

## When to Activate
This skill activates automatically when:
- Creating or modifying files in `src/domain/`, `src/application/`, `src/infrastructure/`, or `src/interfaces/`
- Reviewing code changes across multiple layers
- Adding entities, repositories, use cases, or services

## Quick Checklist

Before approving code, verify:

- [ ] **Dependency Rule**: Dependencies point inward (Domain ← Application ← Infrastructure ← Interfaces)
- [ ] **Entity Independence**: Domain entities have no framework dependencies (no SQLAlchemy, Streamlit, etc.)
- [ ] **Repository Pattern**: All repos inherit from `BaseRepository[T]` and use async/await
- [ ] **DTO Usage**: DTOs used for layer boundaries, not raw entities
- [ ] **Type Safety**: Complete type hints with proper `Optional` handling
- [ ] **Tests**: Unit tests for domain services and use cases

## Core Principles

### 1. Dependency Rule
**Dependencies must point inward: Domain ← Application ← Infrastructure ← Interfaces**

✅ Domain imports nothing from outer layers
✅ Application only imports Domain
✅ Infrastructure imports Domain and Application
✅ Interfaces imports all inner layers (but not other Interface modules)

### 2. Entity Independence
**Domain entities must not depend on external frameworks**

✅ Use `@dataclass` or Pydantic `BaseModel`
❌ No SQLAlchemy models in Domain
❌ No UI framework imports in Domain

### 3. Repository Pattern
**All repositories follow async/await with ISessionAdapter**

✅ Interfaces in Domain: `class IRepo(BaseRepository[T])`
✅ Implementations in Infrastructure: `class RepoImpl(BaseRepositoryImpl[T], IRepo)`
✅ All methods are `async def`

### 4. DTO Pattern
**Always use DTOs between layers**

✅ DTOs in `src/application/dto/`
✅ Input DTO → Use Case → Output DTO
❌ Never expose domain entities directly to outer layers

### 5. Type Safety
**Leverage Python 3.11+ type hints**

✅ All public methods have type hints
✅ Use `T | None` for nullable types
✅ Explicit `None` checks for Optional values

## Common Violations

See [examples.md](examples.md) for detailed good/bad code examples.

## Detailed Reference

For comprehensive architecture guidelines, see [reference.md](reference.md).

## Templates

Use templates in `templates/` directory for creating new:
- Domain entities
- Repository interfaces and implementations
- Use cases with DTOs
- Domain services

## References

- [CLEAN_ARCHITECTURE_MIGRATION.md](../../../docs/CLEAN_ARCHITECTURE_MIGRATION.md)
- [ARCHITECTURE.md](../../../docs/ARCHITECTURE.md)
- [tmp/clean_architecture_analysis_2025.md](../../../tmp/clean_architecture_analysis_2025.md)
