---
name: pattern-review
description: |
  Repository pattern analysis and design.
  Use to evaluate data access code and propose generic repository pattern migration.
  Identifies anti-patterns, duplication, testability issues.
---

# Generic Repository Pattern Analysis

Analyze data access code as a senior software engineer with expertise in ORM frameworks and repository design.

## Input Required

- Existing data access code (controllers, services, direct database calls)
- Current repository implementations (if any)
- Entity/Model definitions
- Tech stack context (ORM, database, framework)

## Analysis Framework

### 1. Anti-Pattern Detection

**Direct ORM/Database Coupling:**
- DbContext/session injected directly into controllers
- Raw SQL scattered across business logic
- Query logic duplicated across services
- No abstraction between domain and persistence

**Repository Smells:**
- Copy-pasted CRUD methods per entity
- Inconsistent method signatures
- Missing common operations (bulk, exists, pagination)
- IQueryable returned leaking ORM details

**Testability Issues:**
- Data access requiring real database for tests
- Missing interfaces preventing mocks
- Tight coupling forcing integration tests only

### 2. Repository Design Evaluation

**Interface Design:**
- Generic constraints (class, entity base)
- Balance generic vs type-safe operations
- Async/sync coverage
- Expression-based filtering

**Common Operations Checklist:**
- GetById, GetAll, Find (with predicate)
- Add, AddRange
- Update, UpdateRange
- Delete, DeleteRange
- Exists, Count
- Pagination support
- Include/eager loading strategy

**Unit of Work Integration:**
- Transaction boundary management
- Multiple repository coordination
- SaveChanges responsibility
- Connection lifetime handling

## Output Format

### Current State Assessment

```markdown
**Data Access Pattern:** [Direct ORM | Specific Repositories | Hybrid | None]
**Entities Requiring Access:** List discovered entities
**Duplication Analysis:** Quantify repeated CRUD patterns
```

### Priority 1: Core Generic Repository Design

```python
# Proposed IGenericRepository interface
class IGenericRepository(Generic[T]):
    def get_by_id(self, id: int) -> Optional[T]: ...
    def get_all(self) -> List[T]: ...
    def find(self, predicate: Callable[[T], bool]) -> List[T]: ...
    def add(self, entity: T) -> T: ...
    def update(self, entity: T) -> T: ...
    def delete(self, entity: T) -> None: ...
    def exists(self, id: int) -> bool: ...
```

### Priority 2: Unit of Work Integration

### Priority 3: Entity-Specific Extensions

### Priority 4: Migration Path

**Phase 1:** Introduce interfaces (non-breaking)
**Phase 2:** Migrate service layer
**Phase 3:** Remove direct DB dependencies
**Phase 4:** Add specification pattern (optional)

### Testing Strategy

Show how to test services with mocked repositories.

## Design Principles

- Don't expose IQueryable - prevents leaky abstraction
- Keep it simple - avoid over-engineering
- Consider your ORM - EF Core vs Dapper need different approaches
- Respect boundaries - repositories return domain objects, not DTOs
- Plan for custom queries - generic doesn't mean inflexible

## What to Avoid

- Overly abstract designs obscuring simple operations
- Ignoring ORM strengths and idioms
- Patterns that hurt query performance
- Unused repository methods
- Forcing async when provider doesn't benefit
