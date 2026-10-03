---
name: architecture
description: "Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale."
---

# Architecture Decision Framework

> "Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale."

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `context-discovery.md` | Questions to ask, project classification | Starting architecture design |
| `trade-off-analysis.md` | ADR templates, trade-off framework | Documenting decisions |
| `pattern-selection.md` | Decision trees, anti-patterns | Choosing patterns |
| `examples.md` | MVP, SaaS, Enterprise examples | Reference implementations |
| `patterns-reference.md` | Quick lookup for patterns | Pattern comparison |

---

## 🔗 Related Skills

| Skill | Use For |
|-------|---------|
| `@[skills/database-design]` | Database schema design |
| `@[skills/api-patterns]` | API design patterns |
| `@[skills/deployment-procedures]` | Deployment architecture |

---

## Core Principle

**"Simplicity is the ultimate sophistication."**

- Start simple
- Add complexity ONLY when proven necessary
- You can always add patterns later
- Removing complexity is MUCH harder than adding it

---

## Validation Checklist

Before finalizing architecture:

- [ ] Requirements clearly understood
- [ ] Constraints identified
- [ ] Each decision has trade-off analysis
- [ ] Simpler alternatives considered
- [ ] ADRs written for significant decisions
- [ ] Team expertise matches chosen patterns


---

# Context Discovery

> Before suggesting any architecture, gather context.

## Question Hierarchy (Ask User FIRST)

1. **Scale**
   - How many users? (10, 1K, 100K, 1M+)
   - Data volume? (MB, GB, TB)
   - Transaction rate? (per second/minute)

2. **Team**
   - Solo developer or team?
   - Team size and expertise?
   - Distributed or co-located?

3. **Timeline**
   - MVP/Prototype or long-term product?
   - Time to market pressure?

4. **Domain**
   - CRUD-heavy or business logic complex?
   - Real-time requirements?
   - Compliance/regulations?

5. **Constraints**
   - Budget limitations?
   - Legacy systems to integrate?
   - Technology stack preferences?

## Project Classification Matrix

```
                    MVP              SaaS           Enterprise
┌─────────────────────────────────────────────────────────────┐
│ Scale        │ <1K           │ 1K-100K      │ 100K+        │
│ Team         │ Solo          │ 2-10         │ 10+          │
│ Timeline     │ Fast (weeks)  │ Medium (months)│ Long (years)│
│ Architecture │ Simple        │ Modular      │ Distributed  │
│ Patterns     │ Minimal       │ Selective    │ Comprehensive│
│ Example      │ Next.js API   │ NestJS       │ Microservices│
└─────────────────────────────────────────────────────────────┘
```


---

# Architecture Examples

> Real-world architecture decisions by project type.

---

## Example 1: MVP E-commerce (Solo Developer)

```yaml
Requirements:
  - <1000 users initially
  - Solo developer
  - Fast to market (8 weeks)
  - Budget-conscious

Architecture Decisions:
  App Structure: Monolith (simpler for solo)
  Framework: Next.js (full-stack, fast)
  Data Layer: Prisma direct (no over-abstraction)
  Authentication: JWT (simpler than OAuth)
  Payment: Stripe (hosted solution)
  Database: PostgreSQL (ACID for orders)

Trade-offs Accepted:
  - Monolith → Can't scale independently (team doesn't justify it)
  - No Repository → Less testable (simple CRUD doesn't need it)
  - JWT → No social login initially (can add later)

Future Migration Path:
  - Users > 10K → Extract payment service
  - Team > 3 → Add Repository pattern
  - Social login requested → Add OAuth
```

---

## Example 2: SaaS Product (5-10 Developers)

```yaml
Requirements:
  - 1K-100K users
  - 5-10 developers
  - Long-term (12+ months)
  - Multiple domains (billing, users, core)

Architecture Decisions:
  App Structure: Modular Monolith (team size optimal)
  Framework: NestJS (modular by design)
  Data Layer: Repository pattern (testing, flexibility)
  Domain Model: Partial DDD (rich entities)
  Authentication: OAuth + JWT
  Caching: Redis
  Database: PostgreSQL

Trade-offs Accepted:
  - Modular Monolith → Some module coupling (microservices not justified)
  - Partial DDD → No full aggregates (no domain experts)
  - RabbitMQ later → Initial synchronous (add when proven needed)

Migration Path:
  - Team > 10 → Consider microservices
  - Domains conflict → Extract bounded contexts
  - Read performance issues → Add CQRS
```

---

## Example 3: Enterprise (100K+ Users)

```yaml
Requirements:
  - 100K+ users
  - 10+ developers
  - Multiple business domains
  - Different scaling needs
  - 24/7 availability

Architecture Decisions:
  App Structure: Microservices (independent scale)
  API Gateway: Kong/AWS API GW
  Domain Model: Full DDD
  Consistency: Event-driven (eventual OK)
  Message Bus: Kafka
  Authentication: OAuth + SAML (enterprise SSO)
  Database: Polyglot (right tool per job)
  CQRS: Selected services

Operational Requirements:
  - Service mesh (Istio/Linkerd)
  - Distributed tracing (Jaeger/Tempo)
  - Centralized logging (ELK/Loki)
  - Circuit breakers (Resilience4j)
  - Kubernetes/Helm
```


---

# Pattern Selection Guidelines

> Decision trees for choosing architectural patterns.

## Main Decision Tree

```
START: What's your MAIN concern?

┌─ Data Access Complexity?
│  ├─ HIGH (complex queries, testing needed)
│  │  → Repository Pattern + Unit of Work
│  │  VALIDATE: Will data source change frequently?
│  │     ├─ YES → Repository worth the indirection
│  │     └─ NO  → Consider simpler ORM direct access
│  └─ LOW (simple CRUD, single database)
│     → ORM directly (Prisma, Drizzle)
│     Simpler = Better, Faster
│
├─ Business Rules Complexity?
│  ├─ HIGH (domain logic, rules vary by context)
│  │  → Domain-Driven Design
│  │  VALIDATE: Do you have domain experts on team?
│  │     ├─ YES → Full DDD (Aggregates, Value Objects)
│  │     └─ NO  → Partial DDD (rich entities, clear boundaries)
│  └─ LOW (mostly CRUD, simple validation)
│     → Transaction Script pattern
│     Simpler = Better, Faster
│
├─ Independent Scaling Needed?
│  ├─ YES (different components scale differently)
│  │  → Microservices WORTH the complexity
│  │  REQUIREMENTS (ALL must be true):
│  │    - Clear domain boundaries
│  │    - Team > 10 developers
│  │    - Different scaling needs per service
│  │  IF NOT ALL MET → Modular Monolith instead
│  └─ NO (everything scales together)
│     → Modular Monolith
│     Can extract services later when proven needed
│
└─ Real-time Requirements?
   ├─ HIGH (immediate updates, multi-user sync)
   │  → Event-Driven Architecture
   │  → Message Queue (RabbitMQ, Redis, Kafka)
   │  VALIDATE: Can you handle eventual consistency?
   │     ├─ YES → Event-driven valid
   │     └─ NO  → Synchronous with polling
   └─ LOW (eventual consistency acceptable)
      → Synchronous (REST/GraphQL)
      Simpler = Better, Faster
```

## The 3 Questions (Before ANY Pattern)

1. **Problem Solved**: What SPECIFIC problem does this pattern solve?
2. **Simpler Alternative**: Is there a simpler solution?
3. **Deferred Complexity**: Can we add this LATER when needed?

## Red Flags (Anti-patterns)

| Pattern | Anti-pattern | Simpler Alternative |
|---------|-------------|-------------------|
| Microservices | Premature splitting | Start monolith, extract later |
| Clean/Hexagonal | Over-abstraction | Concrete first, interfaces later |
| Event Sourcing | Over-engineering | Append-only audit log |
| CQRS | Unnecessary complexity | Single model |
| Repository | YAGNI for simple CRUD | ORM direct access |


---

# Architecture Patterns Reference

> Quick reference for common patterns with usage guidance.

## Data Access Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Active Record** | Simple CRUD, rapid prototyping | Complex queries, multiple sources | Low |
| **Repository** | Testing needed, multiple sources | Simple CRUD, single database | Medium |
| **Unit of Work** | Complex transactions | Simple operations | High |
| **Data Mapper** | Complex domain, performance | Simple CRUD, rapid dev | High |

## Domain Logic Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Transaction Script** | Simple CRUD, procedural | Complex business rules | Low |
| **Table Module** | Record-based logic | Rich behavior needed | Low |
| **Domain Model** | Complex business logic | Simple CRUD | Medium |
| **DDD (Full)** | Complex domain, domain experts | Simple domain, no experts | High |

## Distributed System Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Modular Monolith** | Small teams, unclear boundaries | Clear contexts, different scales | Medium |
| **Microservices** | Different scales, large teams | Small teams, simple domain | Very High |
| **Event-Driven** | Real-time, loose coupling | Simple workflows, strong consistency | High |
| **CQRS** | Read/write performance diverges | Simple CRUD, same model | High |
| **Saga** | Distributed transactions | Single database, simple ACID | High |

## API Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **REST** | Standard CRUD, resources | Real-time, complex queries | Low |
| **GraphQL** | Flexible queries, multiple clients | Simple CRUD, caching needs | Medium |
| **gRPC** | Internal services, performance | Public APIs, browser clients | Medium |
| **WebSocket** | Real-time updates | Simple request/response | Medium |

---

## Simplicity Principle

**"Start simple, add complexity only when proven necessary."**

- You can always add patterns later
- Removing complexity is MUCH harder than adding it
- When in doubt, choose simpler option


---

# Trade-off Analysis & ADR

> Document every architectural decision with trade-offs.

## Decision Framework

For EACH architectural component, document:

```markdown
## Architecture Decision Record

### Context
- **Problem**: [What problem are we solving?]
- **Constraints**: [Team size, scale, timeline, budget]

### Options Considered

| Option | Pros | Cons | Complexity | When Valid |
|--------|------|------|------------|-----------|
| Option A | Benefit 1 | Cost 1 | Low | [Conditions] |
| Option B | Benefit 2 | Cost 2 | High | [Conditions] |

### Decision
**Chosen**: [Option B]

### Rationale
1. [Reason 1 - tied to constraints]
2. [Reason 2 - tied to requirements]

### Trade-offs Accepted
- [What we're giving up]
- [Why this is acceptable]

### Consequences
- **Positive**: [Benefits we gain]
- **Negative**: [Costs/risks we accept]
- **Mitigation**: [How we'll address negatives]

### Revisit Trigger
- [When to reconsider this decision]
```

## ADR Template

```markdown
# ADR-[XXX]: [Decision Title]

## Status
Proposed | Accepted | Deprecated | Superseded by [ADR-YYY]

## Context
[What problem? What constraints?]

## Decision
[What we chose - be specific]

## Rationale
[Why - tie to requirements and constraints]

## Trade-offs
[What we're giving up - be honest]

## Consequences
- **Positive**: [Benefits]
- **Negative**: [Costs]
- **Mitigation**: [How to address]
```

## ADR Storage

```
docs/
└── architecture/
    ├── adr-001-use-nextjs.md
    ├── adr-002-postgresql-over-mongodb.md
    └── adr-003-adopt-repository-pattern.md
```

---
*Generated by [Agent Bridge](https://github.com/HaoNgo232/agent-bridge)*
