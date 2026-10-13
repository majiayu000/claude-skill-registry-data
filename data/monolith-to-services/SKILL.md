---
name: monolith-to-services
description: Decompose a monolith into independent services using bounded context identification, dependency analysis, and incremental extraction strategies. Complements the strangler-fig migration pattern with decomposition heuristics grounded in Domain-Driven Design.
triggers:
  - "break up the monolith"
  - "decompose monolith"
  - "extract service"
  - "bounded context"
  - "service decomposition"
  - "microservices migration"
audience:
  - engineer
  - manager
---

# Monolith to Services

Incrementally extract services from a monolith without rewriting everything at once.

> Pair with the `strangler-fig` skill for the migration execution pattern.
> This skill focuses on *what* to extract and *in what order*.

---

## Step 1: Understand What You Have

Before extracting anything, map the monolith.

### Dependency Analysis
```
1. Generate a module dependency graph (static analysis)
   Tools: Understand, Structure101, CodeScene, or manual
2. Identify tightly coupled clusters (high fan-in / fan-out)
3. Identify loosely coupled modules (candidates for early extraction)
4. Map shared database tables — shared tables = shared ownership problems
```

### Hotspot Analysis
- Which modules change most often together? → Likely belong in the same service
- Which modules are changed by the most teams? → High contention → extract early
- Which modules have the most production incidents? → Isolate to limit blast radius

### Seam Identification (Fowler)
A *seam* is a place where behavior can be changed without modifying the code around it. Find seams to define service boundaries:
- Shared libraries with stable interfaces
- Async jobs that could become separate workers
- External integrations (email, payments, storage) — near-zero cost to extract
- Read-heavy vs write-heavy operations (CQRS opportunity)

---

## Step 2: Define Bounded Contexts

Use Domain-Driven Design to find natural service boundaries.

### Context Mapping
```
For each major domain concept, ask:
- Who owns this data?
- Who can change it?
- What are the invariants (rules that must always hold)?
- What is the consistency boundary?
```

### Context Types
| Context Type | Characteristics | Migration Priority |
|---|---|---|
| **Core Domain** | Competitive advantage, changes often | High — own it cleanly |
| **Supporting Domain** | Enables core, moderate complexity | Medium |
| **Generic Domain** | Commodity (auth, notifications, payments) | Low — buy/SaaS first |

### Bounded Context Template
```
Context: [name]
Core entities: [list]
Owns tables: [list]
Invariants: [business rules]
Changes by: [team or domain]
Integration points: [what other contexts need from this one]
```

---

## Step 3: Prioritize Extraction Order

Not all services are equal to extract. Use this scoring model:

| Factor | Score (1-3) | Weight |
|---|---|---|
| Low coupling to rest of monolith | 1=high coupling, 3=low | 3x |
| Clear ownership / team alignment | 1=unclear, 3=clear | 2x |
| Business value of autonomy | 1=low, 3=high | 2x |
| Data isolation (own tables) | 1=shared, 3=isolated | 2x |
| Team capability to operate it | 1=low, 3=high | 1x |

**Extract highest-scoring contexts first.**

### Common Good First Candidates
- Email / notification service (generic domain, low coupling)
- File/media storage (usually stateless, clear interface)
- Authentication / identity (used everywhere but interface is stable)
- Reporting / analytics (read-only, can lag behind, own DB)
- External integration adapters (payment gateway, shipping API)

### Avoid Extracting First
- Core transactional flows (orders, checkout, billing)
- Anything sharing > 3 tables with other domains
- Anything changed by > 2 teams simultaneously

---

## Step 4: Data Decomposition

Shared databases are the hardest part of monolith extraction.

### Database Decomposition Sequence
1. **Identify table ownership**: Which service *conceptually* owns each table?
2. **Add service-level views**: Create read views for other services while migrating
3. **Duplicate data temporarily**: New service gets its own copy; sync via events during transition
4. **Cut over writes**: New service becomes write owner; old monolith reads via API
5. **Remove old access**: Delete direct DB connections from monolith

### Schema Coupling Patterns to Resolve
| Pattern | Problem | Solution |
|---|---|---|
| Shared mutable table | Two domains write same table | Determine single owner; others use API |
| Integration via DB | Service A reads Service B's DB | Create API or event; remove direct DB access |
| God table | One table has 40+ columns for 3 domains | Split table by domain ownership |
| Distributed transaction | One operation touches 3 services' data | Saga pattern with compensating transactions |

---

## Step 5: Service Interface Design

Before extraction, define the contract:

```markdown
## Service: [name]

**Synchronous API** (for read/query):
- GET /[resource]/{id}
- POST /[resource]

**Events Published** (for state changes):
- [DomainEvent] on [trigger]

**Events Consumed**:
- [DomainEvent] from [source service]

**SLA**:
- p99 latency: [target]
- Availability: [target]

**Ownership**: [team]
**Runbook**: [link]
```

---

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Distributed monolith | Services call each other synchronously in long chains | Redesign with events; reduce runtime coupling |
| Extract by layer | "Frontend service", "database service" | Extract by domain, not technical layer |
| Big bang extraction | Rewrite everything in one shot | Incremental extraction with strangler-fig |
| Nano-services | 50 services for a 10-person team | Team Topologies: one service per stream-aligned team |
| Premature extraction | Splitting before understanding the domain | Run event storming first; don't extract what you don't understand |

---

## Readiness Checklist

Before declaring a service "extracted":
- [ ] Service has its own database / data store
- [ ] Service deploys independently (no coordinated deploys with monolith)
- [ ] Service has its own CI/CD pipeline
- [ ] Service has observability: structured logs, metrics, distributed traces
- [ ] Runbook exists for on-call
- [ ] Monolith no longer imports or directly queries service's data
- [ ] ADR written documenting the boundary decision

---

## References
- Martin Fowler: [Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
- Martin Fowler: [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- Sam Newman: *Building Microservices* (2nd ed.)
- Eric Evans: *Domain-Driven Design*
- LeadDev: [Decomposing the Monolith](https://leaddev.com/technical-direction-strategy)
