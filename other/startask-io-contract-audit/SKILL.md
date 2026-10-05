---
name: startask-io-contract-audit
description: Use when a Startask/Stardust import, prelabel, export, return-flow, or delivery task has an unfrozen customer contract, conflicting specifications/samples/operator trees/platform records/adapter code/validators, mapping/coordinate/timeline/identity/point-order/lineage disagreement, or a delivery-readiness question. Do not use for routine implementation under a confirmed contract or unrelated file conversion.
---

# Startask I/O Contract Audit

## Core rules

- Audit before implementation when the contract is unfrozen or evidence conflicts; code is evidence, not business authority.
- Mark material rows `CONFIRMED`, `INFERRED`, `CONFLICT`, or `MISSING`; never hide unknowns with defaults or fallbacks.
- Do not claim platform or customer success from local validation; redact sensitive customer data and locators.

## Audit workflow

1. Read [references/verification-gates.md](references/verification-gates.md) before stating the first readiness conclusion. Then classify import, prelabel, export, return flow, or acceptance; record data type, mutation, entrypoints, authorization, and planned gate.
2. Inventory six evidence classes—specification, real sample, operator/schema, accepted platform record, adapter code, and validator or accepted output.
3. Compile material rows using [references/contract-matrix.md](references/contract-matrix.md).
4. Give each conflict row exactly one primary layer; split cross-layer issues into linked rows, then select field-specific authority without global precedence.
5. Ask at most three implementation-changing questions; use [references/conflict-and-authority.md](references/conflict-and-authority.md).
6. Freeze approved decisions by completing the `Implementation scope card` in [references/contract-matrix.md](references/contract-matrix.md), then route to an optional Playbook when applicable.
7. Verify G0 through G6 consecutively using [references/verification-gates.md](references/verification-gates.md); report current-turn evidence only.

## Stop conditions

Stop formal implementation and explain the blocker when any of these applies:

- Critical authority evidence that determines business output, remote state, or the requested claim is missing, stale, or conflicting.
- A critical business mapping or missing-value policy remains unresolved.
- A proposed remote mutation is outside the user's authorization or the frozen remote-I/O boundary.
- The requested readiness or delivery claim exceeds the current evidence and verification gate.

For non-critical missing or stale evidence, continue with an `INFERRED` row, record its basis and limitation, and do not promote it to `CONFIRMED`. While a critical blocker remains, continue only safe read-only checks that do not assume the unresolved decision.

## Standard output

Lead with the conclusion and `readiness`, then provide:

1. Task/authorization boundary, evidence manifest, and material matrix.
2. Conflict register, authority, and required decisions.
3. Completed `Implementation scope card`, implementation path or stop reason.
4. `highest_passed_gate`, higher `not_verified`, evidence, blockers, and next step.

Select exactly one `readiness` value from the readiness decision table in [references/verification-gates.md](references/verification-gates.md). If a required check has failed or any critical blocker remains, `BLOCKED` takes precedence regardless of the highest passed gate.

## Route implementation

- For import, prelabel, attachment, `preprocessedData`, or operator/annotation assembly, optionally route to `startask-import-playbook` if available.
- For export, frame splitting, platform semantics, or lineage parsing, optionally route to `startask-export-playbook` if available.
- If unavailable, use repository documents, code, samples, and validators; do not block on personal Skill availability.
- After implementation, return here to re-audit affected rows and gates.

## Read references

- Read [references/contract-matrix.md](references/contract-matrix.md) for evidence, rows, and the `Implementation scope card`.
- Read [references/conflict-and-authority.md](references/conflict-and-authority.md) for `CONFLICT`, `MISSING`, or disagreeing artifacts.
- Read [references/verification-gates.md](references/verification-gates.md) before the first readiness conclusion, then re-read it after scope freeze and before every completion or delivery claim.
- Read [references/case-index-and-evals.md](references/case-index-and-evals.md) only to maintain or validate this Skill.

## Maintain and test this Skill

Exercise the positive and negative cases in [references/case-index-and-evals.md](references/case-index-and-evals.md) after changes. Keep frontmatter triggers-only and regenerate changed UI metadata.
