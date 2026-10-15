---
name: assistant-verification
description: "Analyze proportionate testing, validation, or evaluation for a change, or assess whether existing evidence is sufficient across code, skills, plugins, and non-code artifacts."
---

# Verification Selection And Evidence Assessment

## Contracts

Read contracts/index.yaml first and load matching selectors. Canonical Analysis contracts are contracts/input.yaml, contracts/output.yaml, and contracts/phase-gates.yaml; they remain authoritative. Missing or invalid selectors require the full named contract. Load shared invariants at entry.

## Goal

For a named change, choose credible verification for material claims or assess supplied evidence. Return the canonical evidence_assessment and include verification_decision only for an actionable selection or a carried decision; create no task-state file.

## Success Criteria

- Capture outcome, changes, criteria, boundaries, policy, coverage, and results.
- Select checks for distinct claims and credible failures; name oracles, prerequisites, exclusions, and evidence gaps.
- Assess evidence scope, identity, freshness, and limitations.

## Constraints

- Resolve binding requirements, preferences, and capabilities without waiving mandates. Select scope, technique, and TDD independently: restrictions exclude automated scopes; requirements alone do not.
- Do not invent universal/default counts, ratios, coverage targets, or default TDD. Preserve an explicit binding metric, scope, threshold, and source through a concrete `required_check` and enforcing CheckSpec, or report the policy gap. Zero new tests still needs adequate current/direct evidence.
- Never execute, dispatch, repair, edit, retry, create controllers/ledgers, or replace domain validation, workflow completion, TDD, debugging, independent review, or conditional QA.

## Phases

Use CAPTURE → SELECT → ASSESS → RETURN. Load current_phase at each gate, selection or assessment when needed, and completion before returning. Selection without results is planned; assessment without results remains explicit.

Load only the selected method reference, before relying on it. Each method is linked directly with its trigger:

- [Unit checks](references/methods/unit.md) — isolated behavior or boundary logic.
- [Integration checks](references/methods/integration.md) — cooperating components or a real serialization, storage, configuration, or dependency boundary.
- [End-to-end checks](references/methods/end-to-end.md) — a complete observable user or system journey.
- [Artifact validation](references/methods/artifact-validation.md) — documents, data, configuration, media, or other generated outputs.
- [Behavioral evaluations](references/methods/behavioral-evals.md) — prompts, skills, plugins, agents, or nondeterministic behavior.
- [Property and mutation techniques](references/methods/property-and-mutation.md) — broad input invariants or a specific oracle-quality concern.
- [Performance and resilience checks](references/methods/performance-and-resilience.md) — a stated quality target or credible load/failure concern.

Use references/selection.md for policy, coverage, cost, and stop rules; references/evidence-quality.md for ambiguous, reused, or incomplete evidence. assistant-tdd owns active RED–GREEN–REFACTOR, assistant-debugging owns unknown-cause reproduction, and domain specialists own domain rules.

## Output

Return `verification_decision` only for an actionable selection or a carried decision.
Before Build, visibly return the full actionable decision with CheckSpecs/TddChoice
unchanged. If a binding mandate cannot be represented, omit the actionable decision,
return `evidence_assessment.status=blocked` with the exact conflict, and prevent Build.
Selection-only without results is `planned` with no refs; a requested assessment with
missing or inadequate evidence is `insufficient` or `blocked`, never `planned`. After
results, return actual refs, status, gaps, and exclusions. Workflow carries applicable
keys inline through completion. Missing, failed, stale, partial, skipped, or unavailable
evidence is insufficient or blocked as appropriate.

## Stop Rules

Stop when binding obligations and material claims have credible evidence. Expand for a new gap, change, failure, material risk, request, or binding check. Sufficient does not claim review, delivery approval, or proof of every possible fault.
