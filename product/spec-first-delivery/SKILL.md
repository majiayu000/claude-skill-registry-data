---
name: spec-first-delivery
description: Force plan, HLD, ADRs, and constraints to exist BEFORE any code is generated. Trigger when starting a new feature, epic, or significant change.
---

# Spec-First Delivery

> **Review the spec harder than the code. The cheapest place to be wrong is the spec.**

The harness runs in this order: spec → plan → tasks → code. Skipping the spec is not faster — it is a deferred rewrite.

## When to use

- Any new feature or epic with more than ~1 day of effort
- Infrastructure or architectural changes
- Anything involving a new external dependency, data boundary, or API contract
- Any time an agent offers to "just start coding"

## Procedure

1. **Establish the vision artifact** — confirm the project's vision document exists and is current (e.g. `docs/VISION.md` or equivalent per project structure). If not, create or update it before proceeding.
2. **Write the feature spec** — document: what, why, who (user/actor), constraints, acceptance criteria, and out-of-scope. Reject vague specs ("improve performance") in favour of measurable ones ("p99 latency < 200 ms under 1k rps").
3. **Author or reference the HLD** — a high-level design covering: components affected, data flows, integration points, and failure modes. Diagrams preferred (C4 or sequence).
4. **Create or update ADRs** — one ADR per significant technical decision. Format: Context → Decision → Consequences (trade-offs). Number sequentially (`ADR-NNN`).
5. **Document constraints up front** — security requirements, data residency, budget ceiling, compliance scope, team skill set. Constraints missed here surface as blockers late.
6. **Validate spec completeness** — the spec is done when: acceptance criteria are testable, the failure mode is named, rollback is considered, and cost impact is estimated.
7. **Only then**: generate the implementation plan and tasks. Hand the spec (not a prompt) to the agent.

## Outputs

- `requirements/FEATURE_SPEC.md` (or equivalent per project structure)
- `architecture/decisions/ADR-NNN-<short-title>.md` (one per decision)
- `architecture/HLD-<feature>.md` (if not already covered)
- Updated project roadmap (e.g. `docs/ROADMAP.md` or equivalent per project structure) with new tasks or milestones

## Guardrails

- **No code without a spec.** If an agent begins generating code before a spec exists, stop it and invoke this skill.
- **Loose spec = confident but wrong output.** A vague spec produces plausible-looking, wrong code. Tighten the spec first.
- **Spec is not a prompt.** The spec is a structured document with testable criteria; a prompt is a hint. Do not substitute one for the other.
- **Context efficiency**: Evaluate whether full spec documents are needed, or whether ADRs + plan mode provide sufficient context. Overhead should be proportional to risk.

## Anti-rationalization table

| Excuse the agent makes | Counter |
|---|---|
| "I have enough context to start coding" | No spec = no acceptance criteria = no way to know if the output is correct. Write the spec. |
| "The spec will slow us down" | A missing spec causes rewrites. Rewrites cost more than specs. |
| "The requirements are obvious" | Obvious requirements are the ones most often wrong. Write them down and verify. |
| "We can spec it after the prototype" | Prototypes become production. Spec it now. |
