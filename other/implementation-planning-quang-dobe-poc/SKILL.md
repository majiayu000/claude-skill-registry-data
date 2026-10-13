---
name: implementation-planning
description: Author the mechanical <feature>.plan.md from approved requirement + overview-plan + analyzed. One section per step; final step is the E2E validation gate. No Severity column. Used by the software-engineer agent at /feature:structure stage-2-plan.
---

# Implementation planning skill

## Mission
Author the mechanical implementation plan: concrete substeps with file paths and done-when conditions, one section per implementation step.

## Owned artifact
`docs/<feature>/<feature>.plan.md`. Template: `~/.claude/templates/feature.plan.md`.

## Read scope
- `docs/<feature>/<feature>.requirement.md` (BA's approved output).
- `docs/<feature>/<feature>.overview-plan.md` (Architect's canonical `Step A/B/…` list).
- `docs/<feature>/<feature>.analyzed.md` (Architect's analysis incl. Step Severity table).
- `docs/<feature>/<feature>.test.md` (Tester's `E2E-n` cases — implemented at the final step).
- The plan template; `docs/architecture.md`; project `coding-rules` + `architecture-rules` (context) + soft `docs/narrative/` / `docs/domain/` via `project-seams`.

## Procedure
1. Read the approved requirement, overview-plan, analyzed, plan template, and relevant project rule skills.
2. Write `docs/<feature>/<feature>.plan.md` mirroring the template. One section per implementation step from `overview-plan.md` (`Step A`, `Step B`, …) — **same IDs, same order, no renaming**. Each step lists concrete substeps with file paths, types/methods to create, and done-when conditions.
3. The **final** step of `plan.md` MUST be the **E2E validation gate**: a step that authors automated e2e tests from `<feature>.test.md` and runs them via the project's `test-runner` agent — done-when every `E2E-n` case is green. (Execution lives in the `e2e-validation` skill.)
4. **No Severity column.** `plan.md` is mechanical; per-step Severity lives in `analyzed.md` (Architect, R7). Do not duplicate that table here.
5. Save via `Write`. Hand off per `pipeline-protocol`: "Stage 2-plan complete. Awaiting user APPROVE on `<feature>.plan.md`. After APPROVE, `status.md` is initialized mechanically and `/workflow:step-start <feature>` begins implementation."

## Boundary
Does not author `requirement.md` / `overview-plan.md` / `analyzed.md`, author or modify the Step Severity table, flip `[X]`, or write `status.md`. Full contract: `pipeline-protocol`.
