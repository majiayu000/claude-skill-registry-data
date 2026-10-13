---
name: risk-severity-analysis
description: Author <feature>.analyzed.md including the per-step Severity table (R7). Used by the architect agent at /feature:structure stage-2-analyzed. Severity drives /workflow:step-start --bypass-approval.
---

# Risk & severity analysis skill

> ## R7 — Step Severity rule (verbatim)
>
> *"For every step in the feature's overview-plan, output one row in the Step Severity table inside analyzed.md, each with a declared Severity (minor / medium / major / risky / irreversible). Severity drives /workflow:step-start --bypass-approval. E2E/acceptance cases are not here — they live in the Tester's test.md."*

## Mission
Author the analysis doc and the per-step Severity table that governs auto-approval downstream.

## Owned artifact
`docs/<feature>/<feature>.analyzed.md`. Template: `~/.claude/templates/feature.analyzed.md`.

## Read scope
- The **approved** `<feature>.requirement.md`.
- The **approved** `<feature>.overview-plan.md` — load-bearing: every implementation step there becomes one Severity row.
- The **approved** `<feature>.test.md` (Tester's e2e/acceptance spec) — read it to inform each step's Severity.
- The analyzed template; `docs/architecture.md`; `architecture-rules` + soft `docs/narrative/` / `docs/domain/` via `project-seams`.

## Procedure
1. Read the approved requirement, overview-plan, and test.md. Read the analyzed template.
2. Write `docs/<feature>/<feature>.analyzed.md` mirroring the template: Decision Summary, load-bearing decisions, Risks & Trade-offs, Out-of-Scope Follow-Ups, Project-Specific Rule Overrides (if any), and the Approval Checklist.
3. **Inject a `## N. Step Severity` section before the Approval Checklist.** It MUST be a **2-column** table:

   ```
   | Step ID | Severity |
   |---|---|
   | A | <minor/medium/major/risky/irreversible> |
   | B | ... |
   ```

   Exactly one row per implementation step (`Step A`, `Step B`, …) in `overview-plan.md`. `minor`/`medium` auto-approve under `/workflow:step-start --bypass-approval`; `major`/`risky`/`irreversible` hard-stop and wait for a human. E2E/acceptance cases are NOT here — they live in `<feature>.test.md` (Tester).
4. Save via `Write`. Hand off per `pipeline-protocol`: "Stage 2-analyzed complete. Awaiting user APPROVE on `<feature>.analyzed.md`. After APPROVE, Software Engineer drafts `<feature>.plan.md` at stage-2-plan."

## Boundary
Does not author `overview-plan.md` (that is `architecture-planning`) or `plan.md`, flip `[X]`, modify the requirement, or write `status.md`. Full contract: `pipeline-protocol`.
