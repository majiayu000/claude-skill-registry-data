---
name: playtest-report
description: "Generates or analyzes validation reports. Game: structured playtest report. Product: user-test, API/CLI ergonomics, workflow validation, or adoption-blocker report."
argument-hint: "[new|analyze path-to-notes] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

## User Guide

- When to use: Generates or analyzes validation reports. Game: structured playtest report. Product: user-test, API/CLI ergonomics, workflow validation, or adoption-blocker report.
- Inputs: Command arguments: `/playtest-report [new|analyze path-to-notes] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t3_archive/qa_evidence_index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before generating or analyzing a report:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing playtest report workflow: player comprehension, controls, feel, difficulty, pacing, delight, bugs, and playtest priorities.
- `design/cdd/product-concept.md` -> **[Product]** use this same command as a user-test / workflow validation report: user goal, task completion, API/CLI ergonomics, web flow comprehension, error recovery, latency perception, trust, and adoption blockers.
- If unclear, ask whether the session is a game playtest or a product user/workflow test.

Do not delete playtest examples. Product user-test sections are additional.
## Phase 1: Parse Arguments

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

Determine the mode:

- `new` → generate a blank playtest report template
- `analyze [path]` → read raw notes and fill in the template with structured findings

---

## Phase 2A: New Template Mode

Generate this template and output it to the user:

```markdown
# Playtest Report

## Session Info
- **Date**: [Date]
- **Build**: [Version/Commit]
- **Duration**: [Time played]
- **Tester**: [Name/ID]
- **Platform**: [PC/Console/Mobile]
- **Input Method**: [KB+M / Gamepad / Touch]
- **Session Type**: [First time / Returning / Targeted test]

## Test Focus
[What specific features or flows were being tested]

## First Impressions (First 5 minutes)
- **Understood the goal?

** [Yes/No/Partially]
- **Understood the controls?

** [Yes/No/Partially]
- **Emotional response**: [Engaged/Confused/Bored/Frustrated/Excited]
- **Notes**: [Observations]

## Gameplay Flow
### What worked well
- [Observation 1]

### Pain points
- [Issue 1 -- Severity: High/Medium/Low]

### Confusion points
- [Where the player was confused and why]

### Moments of delight
- [What surprised or pleased the player]

## Bugs Encountered
| # | Description | Severity | Reproducible |
|---|-------------|----------|-------------|

## Feature-Specific Feedback
### [Feature 1]
- **Understood purpose?

** [Yes/No]
- **Found engaging?

** [Yes/No]
- **Suggestions**: [Tester suggestions]

## Quantitative Data (if available)
- **Deaths**: [Count and locations]
- **Time per area**: [Breakdown]
- **Items used**: [What and when]
- **Features discovered vs missed**: [List]

## Overall Assessment
- **Would play again?

** [Yes/No/Maybe]
- **Difficulty**: [Too Easy / Just Right / Too Hard]
- **Pacing**: [Too Slow / Good / Too Fast]
- **Session length preference**: [Shorter / Good / Longer]

## Top 3 Priorities from this session
1. [Most important finding]
2. [Second priority]
3. [Third priority]
```

### Product Validation Template

If the detected domain is Product, generate this template instead:

```markdown
# Product Validation Report

## Session Info
- **Date**: [Date]
- **Build / Commit**: [Version/Commit]
- **Surface**: [API / CLI / web / desktop / mobile / data workflow / docs]
- **Participant / System**: [User role, integrator profile, operator, or CI/system run]
- **Session Type**: [New-user task / Targeted workflow / API integration / CLI ergonomics / Migration dry-run / Adoption-blocker review]

## Validation Focus
[What User Promise, JTBD, workflow, endpoint, command, migration, or docs path was being tested]

## User / Consumer Context
- **Goal**: [What the user or integrator was trying to accomplish]
- **Starting state**: [Account/data/config/env/docs state]
- **Constraints**: [Permissions, platform, package manager, dataset size, network, CI, etc.]

## Workflow Completion
| Step | Expected Outcome | Actual Outcome | Friction | Severity |
|------|------------------|----------------|----------|----------|
| [Step 1] | [Expected] | [Observed] | [None/Low/Med/High] | [S1-S4] |

## API / CLI / Web / Data Findings
### What worked well
- [Observation 1]

### Pain points
- [Issue 1 -- Severity: High/Medium/Low]

### Error recovery
- [Which errors were understandable and which were not]

### Trust and adoption blockers
- [Anything that would prevent real use or integration]

## Quantitative Data (if available)
- **Task completion time**: [Duration]
- **Retries / failed attempts**: [Count]
- **Error count by code**: [List]
- **Latency / throughput**: [Observed values]
- **Rows accepted / rejected**: [Data workflow only]

## Overall Assessment
- **User Promise validated?** [Yes/No/Partially]
- **JTBD completed?** [Yes/No/Partially]
- **Would use again / integrate?** [Yes/No/Maybe]
- **Confidence level**: [Low/Medium/High]

## Top 3 Priorities from this session
1. [Most important workflow or adoption finding]
2. [Second priority]
3. [Third priority]
```

---

## Phase 2B: Analyze Mode

Read the raw notes at the provided path. Cross-reference with existing design documents.
For Game, fill in the playtest template above and flag observations that conflict
with design intent. For Product, fill in the Product Validation Report template
and cross-reference `design/cdd/product-concept.md`, module CDDs, API/CLI/web/data
specs, docs, and acceptance criteria.

---

## Phase 3: Action Routing

Categorize all findings into four buckets:

- **Design changes needed** — fun issues, player confusion, broken mechanics, observations that conflict with the GDD's intended experience
- **Balance adjustments** — numbers feel wrong, difficulty too spiked or too flat
- **Bug reports** — clear implementation defects that are reproducible
- **Polish items** — not blocking progress, but friction or feel issues for later

Present the categorized list, then route:

- **Design changes:** "Run `/propagate-design-change [path]` on the affected design document to find downstream impacts before making changes."
- **Balance adjustments:** "Run `/balance-check [system]` to verify the full balance picture before tuning values."
- **Bugs:** "Use `/bug-report` to formally track these."
- **Polish items:** "Add to the polish backlog in `production/` when the team reaches that phase."

For Product reports, categorize findings into:

- **Product/design changes needed** — User Promise, JTBD, workflow, UX, API, CLI, docs, or data-model gaps
- **Implementation defects** — reproducible bugs, incorrect responses, broken commands, migration failures, build/package defects
- **Reliability/operations issues** — latency, retry/backoff, observability, config, deployment, or rollback gaps
- **Adoption blockers** — confusing docs, error messages, onboarding gaps, permission surprises, trust issues

Route Product findings:

- **Product/design changes:** "Run `/propagate-design-change [path]` on the affected Product CDD or quick spec before changing stories."
- **Implementation defects:** "Use `/bug-report` to formally track these."
- **Reliability/operations issues:** "Run `/perf-profile`, `/security-audit`, or `/team-release` depending on the risk."
- **Adoption blockers:** "Add to `production/qa/evidence/user-tests/` follow-up notes and run `/content-audit` or `/team-ui` if the blocker is docs or interaction clarity."

---

## Phase 3b: Creative Director Player Experience Review

**Review mode check** — apply before spawning CD-PLAYTEST:
- `solo` → skip. Note: "CD-PLAYTEST skipped — Solo mode." Proceed to Phase 4 (save the report).
- `lean` → skip (not a PHASE-GATE). Note: "CD-PLAYTEST skipped — Lean mode." Proceed to Phase 4 (save the report).
- `full` → spawn as normal.

Enter this director handoff only in resolved full review mode. Lean and solo skip
it as stated above; Unknown mode or phase scope stays unresolved. For an actual
Game handoff, read the required Game concept. A skipped review or report filename
does not establish validation.

After categorising findings, spawn `creative-director` via Task using gate **CD-PLAYTEST** (`standards/director-gates.md`).

Pass: the structured report content, game pillars and core fantasy (from `design/cdd/game-concept.md`), the specific hypothesis being tested. For Product, pass product principles, User Promise, JTBD, target workflow, and the structured Product Validation Report.

Present the creative director's assessment before saving the report. If CONCERNS or REJECT, add a `## Creative Director Assessment` section to the report capturing the verdict and feedback. If APPROVE, note the approval in the report.

---

## Phase 4: Save Report

For Game, ask: "May I write this playtest report to `production/qa/evidence/playtests/playtest-[date]-[tester].md`?"

For Product, ask: "May I write this validation report to `production/qa/evidence/user-tests/validation-[date]-[surface].md`?"

If yes, write the file, creating the directory if needed.

When `memory_bank/` exists, update `memory_bank/t3_archive/qa_evidence_index.md`
only within separately covered named index-write authority. Approval to save the
report alone does not authorize that index effect; report-only writes only the
approved report. Preserve original evidence and historical index revisions.

- Keep the full report in `production/qa/evidence/...`.
- Add or update one index row for the evidence path.
- If the same evidence path already exists in the index, update the date,
  evidence type, verdict, and follow-up owner instead of adding a duplicate row.
- Use `playtest` for Game reports and `user-test` or `workflow validation` for
  Product reports.
- Record related story or gate when known; otherwise use `N/A`.

If `memory_bank/` does not exist, do not create it from `/playtest-report`.
Write only the approved evidence report and say: "Run `/constitute` to
establish the memory_bank governance control plane."

---

## Phase 5: Next Steps

Verdict: **COMPLETE** — playtest report generated.

- Act on the highest-priority finding category first.
- After addressing design changes: re-run `/design-review` on the updated CDD.
- After fixing bugs: re-run `/bug-triage` to update priorities.

Product next steps:

- After workflow/product changes: re-run `/design-review` on the affected Product CDD or quick spec.
- After API/CLI/web/data fixes: re-run `/smoke-check` and the relevant contract, CLI, e2e, or migration tests.
- After docs/adoption fixes: run `/content-audit` to confirm examples, help text, and docs match implementation.
