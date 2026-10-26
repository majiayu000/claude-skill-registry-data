---
name: software-architecture
description: Use when designing system structure, evaluating coupling/cohesion, or introducing/integrating new tech into the stack.
---

# Software Architecture

## Modularity

- Build small, independent units that each do one job. Prefer composition of
  small pieces over large multi-purpose modules.

## Coupling & interfaces

- Favor loose coupling: modules interact through explicit, narrow interfaces,
  not shared mutable state or reaching into each other's internals.

## Monolith vs services

- **Modular-monolith is the default** for this app: organize by clear internal
  module boundaries inside one deployable. Peel out a separate service only when
  there's a concrete justification (independent scaling, independent deploy
  cadence, org boundary) — avoid premature microservices.

## Observability

- Design in logs, metrics, and traces for any new subsystem, not bolted on
  after the fact. A feature isn't done until it's debuggable in production.

## Security posture

- Shift-left: security review happens at design time (DevSecOps), not only at
  the code-review gate.
- Apply Zero Trust and least privilege between modules/services — a component
  should only have the access it needs, nothing implicit.
- Practice data minimization: don't store or pass more data than the use case
  needs, especially for financial/PII data.

## External dependencies

- Put an abstraction layer around external/broker/market-data/AI dependencies
  (e.g. IBKR/Freedom Finance data feeds, AI providers) so the app depends on an
  internal interface, not directly on a third-party SDK/shape. This keeps
  provider swaps and testing tractable.

## Applied to this stack

These principles apply concretely to: Next.js 15 (App Router) + Drizzle ORM on
Neon Postgres + better-auth + Vercel. Keep the module boundary between
`services/` (external integration + data access) and `app/`/`components/`
(presentation) intact; don't let Drizzle queries leak into components.

---
Source: wondermentapps.com/blog/software-architecture-best-practices
