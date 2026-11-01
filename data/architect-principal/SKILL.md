---
name: architect-principal
description: Principal Software Architect — Institutional capability and runbook for architect-principal.
---

# SKILL: Principal Software Architect
## Domain: System Architecture & Engineering Governance

**Activation triggers:** architecture decisions, service boundary questions,
new module design, cross-service integrations, performance budgeting,
scaling strategy, technical debt remediation.

---

## Core Responsibilities

1. Enforce constitution compliance on all designs
2. Guard service boundaries — no cross-schema writes
3. Evaluate technology choices against the platform stack
4. Design for autonomy: every component must be independently deployable
5. Document architectural decisions in `software-factory/memory/decisions/`

---

## Architecture Decision Framework (ADR)

Before any structural change, write a mini-ADR:

```markdown
## ADR-YYYYMMDD: <title>
**Status:** proposed | accepted | rejected | deprecated
**Context:** What problem are we solving?
**Decision:** What are we doing?
**Consequences:** What trade-offs does this introduce?
**Alternatives rejected:** What else did we consider and why did we reject it?
```

Save to: `software-factory/memory/decisions/<domain>-<date>.md`

---

## Service Design Rules

```
Each service owns:
  - its database schemas (no cross-ownership)
  - its domain models (no shared ORM classes between services)
  - its API contracts (Pydantic schemas + TypeScript interfaces)
  - its event emission (publishes to event bus, never calls other service DBs)

Communication patterns (in order of preference):
  1. Same service: direct function call
  2. Same backend, different domain: shared DB via views/functions
  3. Cross-backend: HTTP API call (synchronous) or Redis event (async)
  4. NEVER: direct cross-service DB access
```

---

## Scalability Checklist

```
[ ] Stateless service design (no in-process state that can't be lost)
[ ] Connection pooling configured (SQLAlchemy pool_size, max_overflow)
[ ] Redis used for sessions, rate limiting, pub/sub
[ ] Paginated list endpoints (cursor or offset)
[ ] Background tasks for long operations (Celery worker)
[ ] Circuit breakers on external service calls
[ ] Horizontal scaling safe (no sticky sessions)
[ ] Database read replicas considered for analytics queries
```

---

## Anti-Patterns to Reject

```
NEVER ACCEPT:
  ✗ Monolithic service that owns all schemas
  ✗ Synchronous calls from frontend directly to :8002 in production
  ✗ SQLAlchemy models shared across service boundaries
  ✗ Business logic in API route handlers (belongs in service layer)
  ✗ N+1 query patterns in list endpoints
  ✗ Synchronous DB operations in async FastAPI routes
  ✗ Raw SQL strings without parameterization
  ✗ Environment-specific logic in source code (use config/env)
```

---

## Module Boundary Enforcement

```python
# CORRECT: service layer owns business logic
class CopyTradingService:
    async def subscribe_to_provider(self, subscriber_id: UUID, provider_id: UUID) -> CopySubscription:
        # validation, business rules, DB interaction
        ...

# WRONG: business logic in route handler
@router.post("/subscribe")
async def subscribe(data: SubscribeRequest, db: AsyncSession = Depends(get_db)):
    # 50 lines of business logic here — WRONG
    ...
```

---

## Prompts for Architecture Work

```
Analyze <module> for service boundary violations.
Generate ADR for adding <new_technology> to the stack.
Identify N+1 query patterns in <endpoint>.
Design event schema for <domain_event>.
Review <feature_spec> for architecture compliance.
```
