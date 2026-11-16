---
name: kit-design-review
description: Review a proposed design, plan, RFC, or architecture before or during implementation for requirements fit, simpler alternatives, trade-offs, failure modes, operability, and rollout risk, and report a recommendation with concrete concerns. Use when the user asks to review, critique, or sanity-check a design, plan, technical proposal, RFC, or architecture decision, or asks whether an approach is sound. Do not use for reviewing a code diff (use kit-code-review), for security-specific analysis (use kit-threat-model), or for implementing the design (use kit-feature-implementation); this skill reports and does not edit code.
---

# Design review

Report findings without changing code or the design document unless asked.

## 1. Understand the problem

- Restate the goal, users, constraints (scale, latency, cost, deadlines, team skills), and non-goals from the proposal. List requirements the proposal does not address and assumptions it makes.
- Read the code and systems the design touches so the review is grounded in what exists: current data model, interfaces, deployment, and conventions.

## 2. Evaluate

- **Fit:** does the design meet each requirement? Is anything built that no requirement needs?
- **Simpler alternatives:** could an existing component, library, platform feature, or smaller change achieve the goal? Name the alternative and what it gives up.
- **Trade-offs:** consistency and availability, build versus buy, coupling between components, data ownership, and migration cost. Check that the chosen trade-off matches the stated constraints.
- **Failure modes:** what happens on partial failure, retries and duplicates (idempotency), timeouts, overload, and dependency outages; data loss or corruption paths; concurrency and ordering.
- **Operability:** observability, configuration, on-call burden, and how to debug it in production.
- **Change and rollout:** backward compatibility of APIs and data, migration and backfill plan, feature flags, rollback, and how success will be measured.
- **Security and privacy:** note concerns briefly and suggest kit-threat-model when they are significant.

## 3. Report

Start with a recommendation: proceed, proceed with changes, or rethink. Then list concerns ordered by impact, each with the evidence, the consequence, and a concrete suggestion. Include the strongest alternative considered, open questions for the author, and what was out of scope. Keep it specific; skip generic advice that applies to every design.

## Examples

- Use: "Review this RFC for the new billing service." "Is a queue the right approach here?" "Sanity-check my migration plan."
- Skip: "Review my PR." (kit-code-review) "Threat model the upload flow." (kit-threat-model)
