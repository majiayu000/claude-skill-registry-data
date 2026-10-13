---
name: acceptance-spec-authoring
description: Author <feature>.test.md — the black-box e2e/acceptance spec (Given/When/Then, requirement-keyed) from the approved requirement. Planning-only, no source. Used by the tester agent at /feature:structure stage-2-overview.
---

# Acceptance spec authoring skill

## Mission
Author the end-to-end / acceptance test specification from the approved `requirement.md`, **in parallel with** the Architect's overview-plan. Black-box, requirement-keyed, Given/When/Then. Write **no source code**; have **no runtime role** — the Software Engineer later turns these cases into automated e2e tests at the final step of `plan.md`.

## Owned artifact
`docs/<feature>/<feature>.test.md`. Template: `~/.claude/templates/feature.test.md`.

## Read scope
- `docs/<feature>/<feature>.requirement.md` (the approved source of acceptance criteria).
- The test template.
- Optional `docs/narrative/` (product context) and project `test-rules` via `project-seams`.

Do **not** read source code, `docs/domain/`, `docs/architecture.md`, `overview-plan.md`, `analyzed.md`, or `plan.md` — the spec is black-box and requirement-derived. Implementation steps do not exist yet when this is authored.

## Procedure
1. Read the approved `requirement.md` and the test template.
2. Write `docs/<feature>/<feature>.test.md` mirroring the template. One `E2E-n` block per acceptance case, each with `Covers` (the requirement criterion), `Given`, `When`, `Then`. Cover the happy path plus the key error/edge cases the requirement implies. Requirement-keyed only — no step IDs, no `file:line`, no implementation detail.
3. Save via `Write`. Hand off per `pipeline-protocol`: "Stage 2-overview (test spec) complete. Awaiting the combined APPROVE on `<feature>.overview-plan.md` + `<feature>.test.md`."

## Boundary
Writes a markdown spec only — never source. Does not author the Step Severity table (that is `risk-severity-analysis`, R7), other planning artifacts, or `status.md`; has no `/workflow:step-start` or end-of-feature role. Full contract: `pipeline-protocol`.
