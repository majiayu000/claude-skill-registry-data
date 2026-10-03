---
name: architectural-decision-records
description: Use when documenting, drafting, reviewing, or updating ADRs, decision logs, tradeoffs, rationale, consequences, alternatives, or architecture decision history.
license: MIT
compatibility: Codex lazy-loaded skill for OpenSpec projects.
---

# Architectural Decision Records

Use this optional skill only after recommendation and user consent.

An ADR captures one architecturally significant decision, its rationale,
tradeoffs, status, and consequences. Optimize for future maintainers who need
to reconstruct why a decision was made.

## Workflow

1. Identify the single decision. Split bundles into multiple ADRs.
2. Check `preferences.md` for `preferred-style`.
3. If unset, ask the user which style to remember before drafting.
4. Use the matching template in `templates/`.
5. Capture known facts only. Mark missing evidence as `Unknown` or ask a
   focused question.
6. Preserve history. Supersede old accepted ADRs instead of rewriting them away.

## Status Values

- Proposed: under review.
- Accepted: committed decision.
- Deprecated: historically relevant but no longer recommended.
- Superseded: replaced by another ADR.

## Review Checklist

- One decision, not a bundle.
- Context explains why the decision exists.
- Rejected options and tradeoffs are explicit.
- Rationale is tied to requirements and constraints.
- Downsides and follow-up work are recorded.
- Unknowns are marked, not invented.
