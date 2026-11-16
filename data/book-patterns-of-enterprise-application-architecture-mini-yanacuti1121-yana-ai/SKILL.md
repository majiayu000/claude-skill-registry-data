---
name: book--patterns-of-enterprise-application-architecture--mini
description: >-
  PoEAA (Martin Fowler) — Condensed rules — key principles distilled. Use when asked to apply PoEAA principles or review code against PoEAA standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Patterns of Enterprise Application Architecture by Martin Fowler

## When to use

Use when designing or reviewing enterprise application code that crosses presentation, application workflow, domain logic, persistence, transactions, concurrency, integration, session state, or remote boundaries.

## Primary bias to correct

Enterprise applications are not improved by inventing architecture for every feature or by letting the framework, ORM, database schema, or transport shape choose the design. Use a small set of well-understood patterns to make responsibilities and boundaries explicit.

## Decision rules

- Make responsibility ownership explicit before naming patterns: presentation and transport, application workflow, domain logic, data source interaction, transaction management, concurrency control, and integration boundaries must not collapse into one class or layer.
- Use layering as the default organizing principle, but every layer must earn its cost by reducing coupling or clarifying responsibility; forbid lower layers from reaching into presentation concerns and reject pass-through layering theater.
- Choose the business logic pattern by force: Transaction Script for short independent simple flows, Table Module for table-centered set logic, and Domain Model for significant rules, invariants, identity, lifecycle, or collaboration.
- Let Transaction Scripts stay use-case focused, Table Modules stay honestly tabular, and Domain Models own rich behavior; escalate when duplication, lifecycle, or invariant complexity grows.
- Use a Service Layer to define application operations, coordinate use cases, own transaction boundaries and orchestration, expose an application-oriented API, and avoid absorbing all domain logic by default.
- At remote or cross-layer boundaries, use Remote Facade and DTOs to make coarse operations, batching, translation, and transport shape explicit; DTOs are transport structures, not domain models.
- Choose persistence patterns deliberately: repositories speak domain terms and hide query/mapping/storage details, Data Mappers keep SQL and record formats outside domain objects, gateways centralize record/table access, and Active Record is only for simple domains where persistence coupling is acceptable.
- Keep identity, write coordination, and loading behavior visible: use Identity Map for one object per identity per scope, Unit of Work for one logical transactional commit, and Lazy Load only where hidden database or remote chatter will not surprise loops or serializers.
- Choose object-relational mappings by identity, lifecycle, query needs, schema shape, and evolution cost; keep identity fields, foreign keys, association tables, dependent objects, embedded values, serialized values, inheritance mapping, metadata mapping, and query objects explicit rather than accidental.
- Design concurrency and transactions in the application workflow: optimistic locks detect conflicts and surface merge semantics, pessimistic locks require justified contention, transactions stay short, remote calls usually sit outside transactions, and helpers must not hide transaction ownership.
- Use coarse-grained and implicit offline locks only when they preserve a user-level edit without making ownership, contention, or stale-lock cleanup impossible to diagnose.
- Keep presentation code focused on input, rendering, routing, formatting, pagination, UI state, and transport; business rules stay out of controllers, views, templates, and presentation models.
- Access external systems through boundaries, translate partner formats into internal concepts, treat integration events and messages as boundary data, and do not let vendor payloads or serialization code shape internal domain design.
- Choose session state deliberately: client, server, or database session storage must account for integrity, security, scaling, cleanup, durability, server-farm sharing, and database load.
- Use base patterns only for concrete pressure: Gateway for external resources, Mapper for independent sides, Layer Supertype for real shared behavior, Separated Interface for dependency breaks, Registry for controlled well-known objects, Value Object and Money for value semantics, Special Case for repeated null/default behavior, Plugin for runtime extension, Service Stub for remote-service tests, and Record Set when tabular interchange is natural.
- Do not distribute objects or services by default; when distribution is required, separate local object design from the remote contract and budget latency, serialization, versioning, and partial failure.
- Generate code in this order: choose the business logic pattern, place use-case coordination in application services, put rich domain decisions in the domain model, hide persistence behind repositories/mappers/gateways, define transactions explicitly, put DTOs or facades only at boundaries, and keep presentation/transport at the edge.
- Test each responsibility at the level where it owns behavior: domain logic apart from UI and persistence, repositories/mappers/gateways as data infrastructure, services for workflow and transactions, locking where concurrency matters, and DTO/facade mapping at boundaries.

## Trigger rules

- If domain behavior appears in controllers, views, handlers, SQL scripts, triggers, DTOs, framework glue, serialization code, or vendor payload adapters, move it to the owning layer or justify the exception explicitly.
- If one class or layer coordinates rendering, validation, SQL, transactions, domain rules, and external calls, split by responsibility before adding another pattern.
- If a Transaction Script accumulates duplicated decisions, invariants, or lifecycle rules, revisit Domain Model and the supporting persistence pattern.
- If a model is table-shaped in a behavior-rich domain, a repository is generic CRUD, or a service only forwards to persistence, check whether the ORM or database schema has taken over the design.
- If SQL, mapping, transaction ownership, lock acquisition, saves, or external resource access is scattered across callers, introduce the smallest repository, mapper, gateway, Unit of Work, service boundary, or policy that centralizes the rule.
- If lazy loading, duplicate in-memory identities, hidden auto-persistence, N+1 behavior, or ad hoc saves can happen inside one logical work scope, define identity scope, Unit of Work, and loading behavior before continuing.
- If concurrency conflicts, stale locks, user-level edits, or long-running workflows matter, choose explicit optimistic, pessimistic, coarse-grained, or implicit locking semantics instead of relying on informal developer discipline.
- If a remote API looks like local object collaboration, leaks domain internals, or requires many calls per user action, redesign it as a coarse use-case contract with DTO translation.
- If session state has unclear owner, lifetime, storage location, security, scaling, failover, durability, or cleanup behavior, choose the session-state pattern before adding features.
- If a layer exists only to forward calls, a generic repository covers everything, an ORM model doubles as aggregate/service/DTO, or a controller owns the enterprise workflow, treat it as a forbidden-pattern review blocker.

## Final checklist

- Are presentation, workflow, domain, persistence, transaction, concurrency, integration, session, and distribution responsibilities separated intentionally?
- Does the business logic pattern match actual complexity rather than habit or framework shape?
- Are repositories, mappers, gateways, Active Record, Unit of Work, Identity Map, and Lazy Load used only where their forces fit?
- Is transaction ownership explicit, short, and kept out of hidden helpers or remote-call spans?
- Are concurrency conflicts, offline locks, identity scope, and loading behavior visible?
- Are remote and integration boundaries coarse, translated, version-aware, and failure-aware?
- Is session state owned, protected, scalable, durable enough, and cleaned up?
- Are tests aligned to the responsibility that owns each behavior?
