---
name: architecture
description: >-
  Facilitates design decisions and trade-off records. Use when choosing between
  approaches, designing a module or seam, asking "should we use X", or needing
  an architecture decision before coding. Do not use for bug fixes, broad
  tech-debt scans, or greenfield system design from a blank slate.
---

# Architecture

Decide deliberately. Record the *why*. Prefer deepening existing seams over new layers.

## Related skills

- Broad codebase deepening / tech-debt scan → `tech-debt` or `improve-codebase-architecture`
- Greenfield service / API / data model → `system-design`
- Domain grilling with living docs → `grill-with-docs`

## Workflow

1. **Frame the decision** — one-sentence problem; hard constraints (time, security, multi-tenant, platforms).
2. **Read existing truth** — architecture docs, ADRs, prior decisions. Do not re-litigate without new evidence.
3. **List 2–3 options** — each with fit, complexity, testability, reversibility.
4. **Pick and justify** — prefer deep modules (small interface, large behavior) and explicit seams.
5. **Record** — short decision note or ADR. See `references/adr-template.md` for formal ADRs.
6. **Hand off** — implementation tasks must be independently verifiable; no speculative abstractions.

## Constraints

- Do not change user-visible behavior under the guise of “architecture” unless the goal is a behavior change.
- Keep PRs ticket-scoped: architecture work not required for the ticket goes elsewhere.
- Extend canonical modules; do not duplicate contracts or shared helpers.

## Verification

- [ ] Problem and constraints stated
- [ ] ≥2 options considered with trade-offs
- [ ] Decision recorded (PR note or ADR)
- [ ] Next implementation tasks are independently verifiable
