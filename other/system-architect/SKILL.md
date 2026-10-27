---
name: system-architect
description: "High-level system design, Domain-Driven Design boundaries, C4 architecture models, and Architecture Decision Records (ADRs)."
---

# System Architecture & Domain Modeling Protocol

When designing greenfield systems or restructuring existing boundaries, enforce these structural principles.

---

## 1. Domain-Driven Design Boundaries

1. **Bounded Context Separation**:
   - Keep Core Domains, Supporting Domains, and Generic Subdomains decoupled.
   - Modules communicate via explicit interfaces (DTOs, Events, or Public APIs), never by directly mutating internal domain entities.
2. **Aggregates & Invariants**:
   - An Aggregate Root is the sole gateway for external modifications.
   - Enforce business invariants inside the aggregate boundary before dispatching state changes.

---

## 2. Architecture Decision Records (ADRs)

Document significant structural shifts in docs/adr/YYYY-MM-DD-title.md:
- **Context**: The business/technical problem.
- **Decision**: The selected pattern, library, or design.
- **Consequences**: Explicit positive trade-offs and negative technical debt accepted.

---

## 3. C4 Modeling Level 2 (Container Diagrams)

Every service must clearly specify:
- Entrypoints (HTTP API, gRPC, CLI, Worker Consumer).
- Data stores (Transactional DB, Cache, Blob Store).
- Downstream dependencies (Third-party APIs, Message Brokers).
