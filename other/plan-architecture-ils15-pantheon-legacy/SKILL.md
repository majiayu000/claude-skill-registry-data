---
name: plan-architecture
description: Plan feature architecture with component breakdown, data flow, and dependency mapping. Use before implementation to define contracts between layers.
context: fork
globs: ["agents/**", "platform/**", "docs/ARCHITECTURE.md"]
alwaysApply: false
---

# Plan Architecture Skill

## When to Use

Use this skill when:
- Designing a new feature end-to-end before writing code
- Breaking down a complex change into implementation phases
- Mapping dependencies between components
- Defining API contracts between layers
- Evaluating architectural trade-offs
- Preparing a TDD-driven implementation plan

## Architecture Planning Workflow

### 1. Understand the Requirement

Before drawing boxes:
- Identify the **user-facing goal** (what changes for the user?)
- Identify the **system boundary** (what components are touched?)
- Identify **external dependencies** (APIs, databases, queues, third-party services)

### 2. Component Breakdown

Break the feature into layers:

```
Request → Route/Handler → Service → Repository → Database
                       ↓
                   External APIs
```

For each component define:
- **Responsibility** — single sentence
- **Inputs / Outputs** — types, not just names
- **Error cases** — what can go wrong and how it surfaces

### 3. Data Flow Diagram

Map the happy path first, then edge cases:

```
Client
  │ POST /feature
  ▼
Handler (validates input, calls service)
  │
  ▼
Service (business logic, orchestrates)
  │         │
  ▼         ▼
Repo     External API
  │
  ▼
Database
```

### 4. Dependency Map

| Component | Depends On | Depended By |
|-----------|-----------|-------------|
| Handler   | Service   | Client      |
| Service   | Repo, External API | Handler |
| Repo      | Database  | Service     |

### 5. API Contracts

Define contracts before implementation:

```python
# Input schema
class CreateFeatureRequest(BaseModel):
    name: str
    config: dict[str, Any]

# Output schema
class FeatureResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime

# Error cases
# 400 — validation error
# 404 — dependency not found
# 409 — conflict (already exists)
# 500 — upstream failure
```

### 6. Implementation Phases

Split into parallel-safe phases for TDD execution:

```
Phase 1 — Data layer (Demeter)
  - Migration: create table
  - Model: ORM class
  - Repository: CRUD methods + tests

Phase 2 — Service layer (Hermes) [depends on Phase 1]
  - Service class: business logic + tests
  - External API client + mock tests

Phase 3 — API layer (Hermes) [depends on Phase 2]
  - Route handler + tests
  - Request/response schemas

Phase 4 — Frontend (Aphrodite) [can parallel Phase 2+3]
  - Component tree
  - API integration
  - Tests
```

## Architectural Trade-offs Checklist

Before finalizing the plan, evaluate:

- [ ] **Coupling** — are components independently testable?
- [ ] **Reversibility** — can this be rolled back without data loss?
- [ ] **Performance** — any N+1 queries or blocking I/O?
- [ ] **Security** — input validation at boundary? Auth checked?
- [ ] **Observability** — can failures be traced end-to-end?
- [ ] **Scalability** — does this break under 10x load?

## Output Format

The plan output should be a `PLAN-<feature>.md` artifact:

```markdown
# PLAN-<feature>
**Date:** YYYY-MM-DD  **Status:** Awaiting Approval

## Goal
[One sentence]

## Component Breakdown
[Table: Component | Responsibility | Inputs | Outputs]

## Data Flow
[ASCII diagram]

## API Contracts
[Key schemas and error codes]

## Phases
1. Phase 1 — @demeter — [scope]
2. Phase 2 — @hermes — [scope]
3. Phase 3 — @aphrodite — [scope] (parallel with Phase 2)

## Risks
- [Risk and mitigation]

## Open Questions
- [ ] [Decision needed from human]
```
