---
name: book--patterns-of-enterprise-application-architecture--nano
description: >-
  PoEAA (Martin Fowler) — Minimal rules — essential one-liners only. Use when asked to apply PoEAA principles or review code against PoEAA standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Patterns of Enterprise Application Architecture by Martin Fowler

## When to use

Use as a compact always-on compass for enterprise application pattern choices.

## Primary bias to correct

Pattern reuse is not pattern choice. Make responsibilities, persistence, transactions, and remote boundaries explicit before naming a pattern.

## Decision rules

- Keep presentation/transport, application workflow, domain logic, data source interaction, transaction management, concurrency control, and integration boundaries logically separate.
- Choose the business logic pattern by complexity: Transaction Script for simple independent flows, Table Module for table-centered set logic, and Domain Model for rich behavior, invariants, identity, or lifecycle.
- Use Service Layer for use-case coordination and transaction orchestration without turning it into the default home for all domain behavior.
- Match persistence to coupling pressure: Repository/Data Mapper for domain separation, Gateway for record or table access, and Active Record only for simple persistence-coupled domains.
- Make Unit of Work, Identity Map, Lazy Load, transaction boundaries, and lock semantics visible before trusting ORM behavior.
- Keep presentation, DTOs, integration messages, vendor payloads, and serialization code free of business behavior.
- Treat remote boundaries as expensive and failure-prone: use coarse Remote Facade operations, DTO translation, explicit versioning, and partial-failure handling.
- Use session-state and base patterns only for concrete pressure; avoid fake layers, generic repositories, ORM-driven design, controller-centric workflows, and distributed-object illusions.

## Trigger rules

- If one class or layer owns UI, workflow, domain rules, SQL, transactions, and external calls, split responsibility before adding more patterns.
- If a simple Transaction Script grows duplication, invariants, or lifecycle decisions, revisit Domain Model and persistence pattern together.
- If repositories are table-shaped CRUD, models mirror tables in behavior-rich areas, or services only forward calls, check whether the database or ORM has captured the design.
- If lazy loading, duplicate identities, hidden writes, N+1 behavior, ad hoc saves, or unclear locks appear, define identity scope, Unit of Work, loading, and concurrency semantics explicitly.
- If a remote API is chatty, object-shaped, or leaks domain internals, redesign it as a coarse use-case boundary with DTO translation.

## Final checklist

- Right business logic and persistence pattern for actual complexity?
- Explicit layer, transaction, identity, loading, lock, session, and integration ownership?
- Business rules kept out of UI, DTOs, integration, and serialization?
- Remote boundary coarse, translated, version-aware, and failure-aware?
