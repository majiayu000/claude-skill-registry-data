---
name: system-design
description: >-
  Designs services, APIs, and data models from requirements. Use when designing
  a new service, API, or data model, or when doing system design for a greenfield
  or major new capability. Do not use for a small local design choice inside an
  existing module (use architecture).
---

# System Design

Turn requirements into a coherent design: boundaries, contracts, data, and failure modes.

## Workflow

1. **Requirements** — functional goals, non-functionals (latency, consistency, tenancy, offline), explicit non-goals.
2. **Context** — actors, existing systems, trust boundaries. Sketch a simple topology.
3. **Contracts** — public APIs/events first (schemas, errors, versioning). See `references/design-checklist.md`.
4. **Data** — entities, ownership, consistency model, migrations story.
5. **Failure & scale** — timeouts, retries/idempotency, backpressure, authn/z, observability.
6. **Options** — 2 approaches with trade-offs; pick one; list open questions.
7. **Hand off** — ADRs for major decisions; implementation slices that are testable.

## Constraints

- Design for operability (health, logs, metrics) not only happy path.
- Prefer boring technology that fits the existing stack unless requirements force otherwise.
- Do not over-design for hypothetical scale.

## Verification

- [ ] Requirements and non-goals written
- [ ] Topology + trust boundaries clear
- [ ] API/data contracts sketched
- [ ] Failure modes and auth addressed
- [ ] Decision + open questions recorded
