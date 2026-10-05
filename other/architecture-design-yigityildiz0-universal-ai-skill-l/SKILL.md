---
name: architecture-design
description: "System architecture design including requirements analysis, trade-off evaluation, ADRs, and system decomposition. Use when designing new systems, evaluating architectures, or documenting design decisions. Turkish triggers: sistem mimarisi tasarla, mimari karar, bileşenleri ayır, teknik trade-off."
---

# Architecture Design

Structured guidance for designing software architectures, from requirements elicitation through system decomposition, trade-off analysis, and decision documentation using industry-standard frameworks like C4, ATAM, and Architecture Decision Records.

## When to Use This Skill

Use this skill for:

- Designing a new system or major subsystem from scratch
- Evaluating competing architectural approaches for a project
- Documenting architecture decisions with ADRs
- Decomposing a monolithic system into well-defined components
- Conducting architecture reviews or fitness function checks
- Analyzing quality attribute trade-offs (performance vs. consistency, availability vs. partition tolerance)
- Creating C4 diagrams at context, container, component, or code levels
- Establishing architecture governance and review processes

**Trigger phrases**: "architecture design", "system design", "ADR", "architecture decision record", "C4 model", "trade-off analysis", "system decomposition", "quality attributes", "architecture review", "fitness function"

## What This Skill Does

Provides architecture design patterns including:

- **Requirements Analysis**: Stakeholder identification, quality attribute scenarios, constraint cataloging
- **Trade-off Evaluation**: CAP theorem reasoning, consistency vs. availability matrices, cost vs. performance analysis
- **System Decomposition**: Layered, hexagonal, onion, clean architecture strategies
- **Decision Documentation**: ADR templates, decision logs, rationale capture
- **Visual Modeling**: C4 model at all four levels (context, container, component, code)
- **Fitness Functions**: Automated architecture governance via measurable checks
- **Dependency Analysis**: Coupling metrics, dependency inversion, acyclic dependency graphs
- **Scalability Patterns**: Horizontal vs. vertical scaling, caching tiers, read replicas, sharding strategies

## Instructions

### Step 1: Elicit Requirements and Constraints

Before designing anything, gather the inputs that constrain the solution space.

**Stakeholder Map**:

| Stakeholder | Concern | Priority |
|-------------|---------|----------|
| Product Owner | Feature velocity, time to market | High |
| Operations | Uptime, deployment simplicity, observability | High |
| Security | Data protection, compliance, least privilege | High |
| Developers | Code maintainability, testability, developer experience | Medium |
| Finance | Infrastructure cost, licensing | Medium |

**Quality Attribute Scenario Template**:

```
Source:       [Who or what triggers the scenario]
Stimulus:     [The event or condition]
Artifact:     [The component affected]
Environment:  [Under what conditions]
Response:     [What the system does]
Measure:      [How we know it succeeded]
```

**Example Quality Attribute Scenarios**:

```
# Performance
Source:       End user
Stimulus:     Submits a search query
Artifact:     Search service
Environment:  Normal operation, 10K concurrent users
Response:     Returns results
Measure:      95th percentile latency < 200ms

# Availability
Source:       Monitoring system
Stimulus:     Primary database node fails
Artifact:     Order processing service
Environment:  Peak traffic (Black Friday)
Response:     Fails over to replica, no dropped transactions
Measure:      99.95% uptime over a rolling 30-day window

# Security
Source:       External attacker
Stimulus:     Attempts SQL injection on login endpoint
Artifact:     Authentication service
Environment:  Normal operation
Response:     Input sanitized, attempt logged, IP rate-limited
Measure:      Zero successful injections in penetration tests
```

**Constraint Catalog**:

```markdown
## Technical Constraints
- Must run on AWS (existing enterprise agreement)
- Must support PostgreSQL 15+ (DBA team expertise)
- Must integrate with existing LDAP for authentication

## Business Constraints
- MVP must launch within 6 months
- Team of 4 backend engineers, 2 frontend engineers
- Annual infrastructure budget: $120K

## Regulatory Constraints
- GDPR compliance required (EU customer data)
- PCI DSS Level 2 (payment processing)
- Data residency: EU region only
```

### Step 2: Analyze Quality Attribute Trade-offs

Use structured analysis to reason about competing quality attributes.

**CAP Theorem Decision Matrix**:

| Scenario | Choose CP | Choose AP | Rationale |
|----------|-----------|-----------|-----------|
| Financial transactions | Yes | No | Consistency critical; stale balances cause real losses |
| Social media feed | No | Yes | Availability preferred; eventual consistency acceptable |
| Inventory management | Yes | No | Overselling is worse than temporary unavailability |
| User session store | No | Yes | Stale session data tolerable; downtime is not |
| Configuration service | Yes | No | All nodes must agree on config to avoid split behavior |

**Trade-off Analysis Template**:

```markdown
## Trade-off: [Attribute A] vs. [Attribute B]

### Context
[Describe the architectural decision that forces this trade-off]

### Option 1: Favor [Attribute A]
- **Approach**: [Technical approach]
- **Gains**: [What improves]
- **Costs**: [What degrades]
- **Risk**: [What could go wrong]

### Option 2: Favor [Attribute B]
- **Approach**: [Technical approach]
- **Gains**: [What improves]
- **Costs**: [What degrades]
- **Risk**: [What could go wrong]

### Decision
[Which option and why, referencing quality attribute scenarios]
```

**Example: Consistency vs. Latency for a Product Catalog**:

```markdown
## Trade-off: Consistency vs. Latency

### Context
Product catalog serves 50K RPM. Prices update ~100 times/day.
Stale prices could cause revenue loss or customer complaints.

### Option 1: Favor Consistency (read-through cache)
- **Approach**: Cache with short TTL (5s), invalidate on write
- **Gains**: Prices always within 5s of truth
- **Costs**: Higher p99 latency (~80ms vs ~5ms), more DB load
- **Risk**: Cache stampede under high traffic

### Option 2: Favor Latency (eventual consistency)
- **Approach**: CDN cache with 60s TTL, async invalidation via events
- **Gains**: p99 < 10ms, reduced DB load by 95%
- **Costs**: Prices stale up to 60s after update
- **Risk**: Customer sees old price, checks out at new price

### Decision
Option 2 with a price-lock guarantee at checkout. Stale catalog
display is acceptable; the cart service validates current prices
before charging. This gives us sub-10ms reads without revenue risk.
```

### Step 3: Decompose the System

Choose a decomposition strategy that aligns with team structure and quality attributes.

**Layered Architecture** (traditional, good for CRUD-heavy apps):

```
┌─────────────────────────────────┐
│       Presentation Layer        │  UI, API controllers
├─────────────────────────────────┤
│       Application Layer         │  Use cases, orchestration
├─────────────────────────────────┤
│         Domain Layer            │  Business rules, entities
├─────────────────────────────────┤
│       Infrastructure Layer      │  DB, messaging, external APIs
└─────────────────────────────────┘
```

**Hexagonal Architecture** (ports and adapters, good for testability):

```
                    ┌──────────────┐
   HTTP Adapter ──> │              │ <── Database Adapter
                    │   Domain     │
  gRPC Adapter ──> │   (Ports &   │ <── Message Queue Adapter
                    │    Core)     │
   CLI Adapter ──> │              │ <── File System Adapter
                    └──────────────┘
```

**Hexagonal Architecture in Code**:

```python
# domain/ports.py - Define ports (interfaces)
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Order:
    id: str
    customer_id: str
    total: float
    status: str

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None: ...

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, customer_id: str, amount: float) -> bool: ...

# domain/services.py - Core business logic (no framework imports)
class OrderService:
    def __init__(self, repo: OrderRepository, payments: PaymentGateway):
        self._repo = repo
        self._payments = payments

    def place_order(self, order: Order) -> Order:
        if order.total <= 0:
            raise ValueError("Order total must be positive")
        charged = self._payments.charge(order.customer_id, order.total)
        if not charged:
            raise RuntimeError("Payment failed")
        order.status = "confirmed"
        self._repo.save(order)
        return order

# adapters/postgres_repo.py - Infrastructure adapter
class PostgresOrderRepository(OrderRepository):
    def __init__(self, connection_pool):
        self._pool = connection_pool

    def save(self, order: Order) -> None:
        with self._pool.connection() as conn:
            conn.execute(
                "INSERT INTO orders (id, customer_id, total, status) "
                "VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (id) DO UPDATE SET status = %s",
                (order.id, order.customer_id, order.total,
                 order.status, order.status),
            )

    def find_by_id(self, order_id: str) -> Order | None:
        with self._pool.connection() as conn:
            row = conn.execute(
                "SELECT id, customer_id, total, status FROM orders WHERE id = %s",
                (order_id,),
            ).fetchone()
            return Order(*row) if row else None
```

### Step 4: Document Decisions with ADRs
Read [references/adr-guidance.md](references/adr-guidance.md) when an architecture decision needs a durable ADR, alternatives, or consequence analysis.

### Step 5: Create C4 Model Diagrams

The C4 model provides four levels of zoom for communicating architecture.

**Level 1: System Context Diagram** (who uses the system, what does it connect to):

```
┌─────────────────────────────────────────────────────┐
│                   E-Commerce Platform               │
│                                                     │
│  ┌─────────┐   ┌──────────┐   ┌─────────────────┐  │
│  │ Web App │   │ Mobile   │   │ Admin Dashboard  │  │
│  │ (React) │   │ (Flutter)│   │ (React)          │  │
│  └────┬────┘   └────┬─────┘   └───────┬─────────┘  │
│       │              │                 │             │
│       └──────────────┼─────────────────┘             │
│                      │                               │
│              ┌───────▼───────┐                       │
│              │  API Gateway  │                       │
│              └───────┬───────┘                       │
│                      │                               │
└──────────────────────┼───────────────────────────────┘
                       │
        ┌──────────────┼──────────────────┐
        │              │                  │
  ┌─────▼─────┐  ┌─────▼──────┐  ┌───────▼──────┐
  │ Payment   │  │ Shipping   │  │ Email        │
  │ Provider  │  │ Partner    │  │ Service      │
  │ (Stripe)  │  │ (FedEx)    │  │ (SendGrid)  │
  └───────────┘  └────────────┘  └──────────────┘
```

**Level 2: Container Diagram** (major deployable units):

```
┌───────────────────────────────────────────────────┐
│                  API Gateway (Kong)                │
└───────┬──────────────┬───────────────┬────────────┘
        │              │               │
┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼───────┐
│ Order Service│ │ Catalog   │ │ User Service │
│ (Go)         │ │ Service   │ │ (Go)         │
│              │ │ (Python)  │ │              │
└───────┬──────┘ └─────┬─────┘ └──────┬───────┘
        │              │               │
┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼───────┐
│ Orders DB    │ │ Catalog DB│ │ Users DB     │
│ (PostgreSQL) │ │ (MongoDB) │ │ (PostgreSQL) │
└──────────────┘ └───────────┘ └──────────────┘
```

**Level 3: Component Diagram** (internal structure of a container):

```
┌──────────────────────────────────────────────┐
│              Order Service                    │
│                                              │
│  ┌────────────────┐  ┌───────────────────┐   │
│  │ REST Controller│  │ gRPC Handler      │   │
│  └───────┬────────┘  └───────┬───────────┘   │
│          │                   │               │
│          └─────────┬─────────┘               │
│                    │                         │
│          ┌─────────▼──────────┐              │
│          │  Order Use Cases   │              │
│          │  (Application)     │              │
│          └─────────┬──────────┘              │
│                    │                         │
│     ┌──────────────┼──────────────┐          │
│     │              │              │          │
│  ┌──▼─────┐  ┌─────▼─────┐  ┌────▼──────┐   │
│  │ Order  │  │ Payment   │  │ Event     │   │
│  │ Repo   │  │ Client    │  │ Publisher │   │
│  └────────┘  └───────────┘  └───────────┘   │
└──────────────────────────────────────────────┘
```

### Step 6: Define Architecture Fitness Functions
Read [references/fitness-functions.md](references/fitness-functions.md) when architecture constraints should be executable or CI-enforced.

## Best Practices

- **Start with quality attributes, not technology** - Let requirements drive architecture, not vendor preference
- **Document every significant decision** - ADRs pay dividends during onboarding and audits
- **Validate continuously** - Architecture fitness functions catch drift before it compounds
- **Separate what changes from what stays stable** - Identify axes of change and draw boundaries there
- **Prefer composition over inheritance** - In architecture, this means small, composable services over monolithic frameworks
- **Design for failure** - Every network call can fail; every disk can fill; every dependency can slow down
- **Make the implicit explicit** - If a constraint exists only in someone's head, it will be violated
- **Minimize coupling, maximize cohesion** - Components that change together should live together
- **Defer irreversible decisions** - Use abstractions to buy time on technology choices
- **Review architecture regularly** - Schedule quarterly fitness reviews, not just code reviews

## Common Patterns
Read [references/common-patterns.md](references/common-patterns.md) when choosing migration, BFF, anti-corruption, or related architecture patterns.

## Quality Checklist

- [ ] Quality attribute scenarios documented for top 5 concerns
- [ ] Trade-off analysis completed for each contested decision
- [ ] ADR written for every significant architectural choice
- [ ] C4 context and container diagrams created and current
- [ ] Component boundaries align with team boundaries (Conway's Law)
- [ ] Dependency direction verified (always toward the domain)
- [ ] Fitness functions implemented and running in CI
- [ ] Scalability analysis completed (10x current load)
- [ ] Failure mode analysis documented (what happens when X goes down?)
- [ ] Security threat model completed (STRIDE or equivalent)
- [ ] Data flow diagrams created for sensitive data paths
- [ ] Architecture reviewed by at least one peer

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We can design architecture as we go" | Systems built without upfront architecture routinely encounter the distributed monolith anti-pattern — services that are physically separate but logically coupled, requiring synchronized deployments and producing more downtime than a true monolith. |
| "ADRs are just documentation overhead" | Without recorded decisions, teams revisit the same trade-offs repeatedly; the hidden cost is re-litigating choices (e.g., sync vs. async, SQL vs. NoSQL) in every planning session instead of once. |
| "We can scale later when it's needed" | Adding horizontal scalability after the fact requires changing session management, introducing distributed caches, and splitting state — changes that can take months for an established system (e.g., Reddit's years-long migration from a non-distributed architecture). |
| "C4 diagrams are too formal for our team size" | Diagrams are primarily for onboarding and incident response, not the team that built the system; teams that skip them consistently report longer mean-time-to-diagnose during outages. |
| "Quality attributes are implicit in good code" | Performance, availability, and security have conflicting implementation strategies; without explicit quality attribute scenarios (e.g., "99.9% uptime during region failure"), teams optimize for the wrong constraints and discover the conflict in production. |
| "We'll document the architecture after we build it" | Post-hoc documentation captures what was built, not why; ADRs written retroactively cannot capture the rejected alternatives and constraints that motivated each decision. |

## Verification

- [ ] C4 context and container diagrams exist and show all external systems and inter-container communication
- [ ] At least one ADR exists per major architectural decision (data store choice, sync/async boundary, deployment target)
- [ ] Quality attribute scenarios are documented with measurable targets (e.g., "p99 latency < 200 ms at 1,000 RPS")
- [ ] CAP theorem trade-offs are documented for every data store that participates in multi-node deployment
- [ ] Failure mode analysis covers what happens when each external dependency or service is unavailable
- [ ] Security threat model (STRIDE or equivalent) identifies at least the top three attack surfaces

## Related Skills

- `ddd-strategic-design` - Domain modeling and bounded context identification
- `api-design` - API contract design for inter-component communication
- `microservices-patterns` - Distributed system patterns and resilience
- `cloud-architect` - Cloud-native architecture and managed service selection
- `security-review` - Security architecture assessment

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
