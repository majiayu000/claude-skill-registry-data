---
name: step-execution
description: Execute the substeps of one implementation step — edit the named files, author unit tests, self-verify, and report. Used by the software-engineer agent at /workflow:step-start. Concrete build/test commands are delegated to the project test-runner.
---

# Step execution skill

## Mission
Execute one implementation step from `plan.md`: edit the named files, author its unit tests, stay inside the substeps, and self-verify before handing back to the user.

## Inputs
- Feature name and the Step `<ID>` (e.g. `A`, `B`).
- The Step `<ID>` section in `docs/<feature>/<feature>.plan.md`.
- The matching Severity row in `docs/<feature>/<feature>.analyzed.md` (2-col `Step ID | Severity`; the cell `/workflow:step-start --bypass-approval` consults).

## Read scope
- The plan section + Severity row above.
- Production source (read + write — the only role that writes source).
- Project `coding-rules` (+ `architecture-rules` for context, `test-rules` for unit-test layout) + soft `docs/narrative/` / `docs/domain/` via `project-seams`.

## Procedure
1. Read the Step `<ID>` section in `plan.md` and the matching Severity row in `analyzed.md`.
2. Execute the substeps **in order**, editing the named files. Author unit tests for the step's logic alongside the production code (layout per the project's `test-rules`). Stay inside the substeps — do not invent extra work. The Tester is not spawned per step; the SE owns all test code.
3. If this is the **final** step (the E2E validation gate), additionally follow the `e2e-validation` skill.
4. Self-verify the change before reporting — stack-agnostic gate, in order, stopping at the first failure: build → type-check → lint → unit tests → secret/debug scan → diff review. Run concrete commands via the project `test-runner` agent when present; if the project ships no build/test, note that and rely on the diff review.
5. Return a brief chat summary: files changed and what to verify before the user types `APPROVE`.

## Boundary
Does not flip `[X]` (main Claude does that via `/workflow:step-approve`), author or modify planning artifacts / the Severity table, write `status.md`, or commit. Full contract: `pipeline-protocol`.
