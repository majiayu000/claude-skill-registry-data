---
name: documentation
description: "Document WHY not just WHAT: README, setup, arch, ADRs, API contracts, runbooks."
---

# documentation

Write the decision, not the code: WHY it is this way, what was rejected, how to operate it.

## Activate when

- Shipping features, making architectural decisions, changing APIs, or onboarding the next reader (human or agent).

## Do NOT activate for

- Code comments explaining WHAT (rename instead); marketing copy.

## Inspection

Find what a new reader needs: setup path, architecture map, decision history (ADRs?), API contracts, runbooks. Note what's missing or stale.

## Decision rules

- README: setup in under 10 minutes, verified by following it cold.
- ADRs: one per significant decision — context, options, decision, consequences; rejected alternatives recorded (they prevent re-litigation).
- API docs generated from code + examples; changelogs per release; runbooks per alert (symptom → diagnosis → fix → escalate).
- Docs live with code and are reviewed in the same PR; stale docs are worse than none — delete or fix on sight.

## Procedure

1. Write the missing piece at the right level (README/setup/arch/ADR/contract/runbook).
2. Verify setup docs by executing them; verify runbooks by drill.
3. Keep docs versioned with the code they describe; prune on every migration.
4. Verify: a fresh reader (or agent) completes setup and finds answers without asking.

## Failure modes

- WHAT-only comments; ADRs written after the fact as justification; runbooks without commands; setup docs that never worked; documentation drift after refactors.

## Escalation

Research-heavy docs (migrations, compat) → research/documentation-search for version facts.

## References

- Related: `../requirements-analysis/` (ADRs live here conceptually), `../../github/pr-workflow/` (PR descriptions), `../../backend/production-readiness/` (runbooks).
