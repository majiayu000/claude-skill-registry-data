---
name: book--implementing-domain-driven-design--nano
description: >-
  Implementing DDD (Vaughn Vernon) — Minimal rules — essential one-liners only. Use when asked to apply Implementing DDD principles or review code against Implementing DDD standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Implementing Domain-Driven Design by Vaughn Vernon

## When to use

Use when tight context still needs DDD guardrails for context leakage, fake tactical patterns, Aggregate sprawl, and cross-context model coupling.

## Primary bias to correct

Local context, language, and invariants outrank reuse pressure, ORM convenience, object graph traversal, and framework or client shape.

## Decision rules

- Name the Bounded Context and local Ubiquitous Language before interpreting models, services, repositories, events, APIs, persistence, or integrations.
- Translate across contexts and foreign systems; never share local Aggregates, Entities, enums, or domain objects as integration contracts.
- Treat Aggregates as small immediate consistency boundaries with one root, hidden mutable internals, identity references to other Aggregates, and eventual consistency outside one boundary by default.
- Use Entities for identity and lifecycle, Value Objects for immutable validated descriptive values, and Domain Services only when no model object naturally owns the operation.
- Keep Repositories focused on Aggregate Roots and Application Services focused on use-case coordination rather than domain decisions.
- Publish Domain Events only as meaningful completed past-tense facts; use Event Sourcing only when event history is the right persistence model.
- Use DTOs, projections, use-case queries, adapters, and explicit scope identifiers instead of exposing or reshaping domain internals for clients.

## Trigger rules

- When a term is ambiguous, generic, or reused across contexts, split or qualify it by Bounded Context before coding.
- When one transaction or object graph wants multiple Aggregate roots, demand immediate-invariant proof; otherwise coordinate by identity, events, policies, processes, or Application Services.
- When foreign models, database shape, framework objects, transport payloads, UI needs, or another context's model leak into domain code, translate at the boundary.
- When DDD vocabulary appears around CRUD services, generic repositories, mutable graphs, or anemic models, require the real invariant and behavior or simplify the design.
- When reviewing DDD code, verify context, language, Aggregate boundary, translation, Repository shape, events-as-facts, and Application Service thinness before approving.

## Final checklist

- Clear Bounded Context and local language?
- Explicit translation instead of shared model types?
- Aggregate boundary backed by immediate invariants?
- Identity references across Aggregates?
- Repositories Aggregate-root focused?
- Application Services coordinating, not deciding?
- Client, persistence, and foreign concerns kept outside the domain model?
