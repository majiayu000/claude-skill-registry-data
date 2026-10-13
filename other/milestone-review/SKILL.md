---
name: milestone-review
description: "Generates a comprehensive milestone progress review including feature completeness, quality metrics, risk assessment, and go/no-go recommendation. Use at milestone checkpoints or when evaluating readiness for a milestone deadline."
argument-hint: "[milestone-name|current] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

## User Guide

- When to use: Generates a comprehensive milestone progress review including feature completeness, quality metrics, risk assessment, and go/no-go recommendation. Use at milestone checkpoints or when evaluating readiness for a milestone deadline.
- Inputs: Command arguments: `/milestone-review [milestone-name|current] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t3_archive/sprint_snapshots/milestone-[name]-review-[YYYY-MM-DD].md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before reviewing a milestone:
- `design/cdd/game-concept.md` -> **[Game]** review milestone progress against player experience, content completeness, playtest evidence, game CDDs, platform readiness, and release goals.
- `design/cdd/product-concept.md` -> **[Product]** review milestone progress against user value, workflow completion, API/CLI/UI readiness, test evidence, operational readiness, docs, and release goals.
- If unclear, present both review lenses and ask the user to pick one.

Game milestone review criteria remain valid; product criteria are a parallel lens.
## Phase 0: Parse Arguments

Extract the milestone name (`current` or a specific name) and resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

---

## Phase 1: Load Milestone Data

Read the milestone definition from `production/milestones/`. If the argument is `current`, use the most recently modified milestone file.

Read all sprint reports for sprints within this milestone from `production/sprints/`.

---

## Phase 2: Scan Codebase Health

- Scan for `TODO`, `FIXME`, `HACK` markers that indicate incomplete work
- Check the risk register at `production/risk-register/`

---

## Phase 3: Generate the Milestone Review

```markdown
# Milestone Review: [Milestone Name]

## Overview
- **Target Date**: [Date]
- **Current Date**: [Today]
- **Days Remaining**: [N]
- **Sprints Completed**: [X/Y]

## Feature Completeness

### Fully Complete
| Feature | Acceptance Criteria | Test Status |
|---------|-------------------|-------------|

### Partially Complete
| Feature | % Done | Remaining Work | Risk to Milestone |
|---------|--------|---------------|------------------|

### Not Started
| Feature | Priority | Can Cut? | Impact of Cutting |
|---------|----------|----------|------------------|

## Quality Metrics
- **Open S1 Bugs**: [N] -- [List]
- **Open S2 Bugs**: [N]
- **Open S3 Bugs**: [N]
- **Test Coverage**: [X%]
- **Performance**: [Within budget? Details]

## Code Health
- **TODO count**: [N across codebase]
- **FIXME count**: [N]
- **HACK count**: [N]
- **Technical debt items**: [List critical ones]

## Risk Assessment
| Risk | Status | Impact if Realized | Mitigation Status |
|------|--------|-------------------|------------------|

## Velocity Analysis
- **Planned vs Completed** (across all sprints): [X/Y tasks = Z%]
- **Trend**: [Improving / Stable / Declining]
- **Adjusted estimate for remaining work**: [Days needed at current velocity]

## Scope Recommendations
### Protect (Must ship with milestone)
- [Feature and why]

### At Risk (May need to cut or simplify)
- [Feature and risk]

### Cut Candidates (Can defer without compromising milestone)
- [Feature and impact of cutting]

## Go/No-Go Assessment

**Recommendation**: [GO / CONDITIONAL GO / NO-GO]

**Conditions** (if conditional):
- [Condition 1 that must be met]
- [Condition 2 that must be met]

**Rationale**: [Explanation of the recommendation]

## Action Items
| # | Action | Owner | Deadline |
|---|--------|-------|----------|
```

---

## Phase 3b: Producer Risk Assessment

**Review mode check** — apply before spawning PR-MILESTONE:
- `solo` → skip. Note: "PR-MILESTONE skipped — Solo mode." Present the Go/No-Go section without a producer verdict.
- `lean` → skip (not a PHASE-GATE). Note: "PR-MILESTONE skipped — Lean mode." Present the Go/No-Go section without a producer verdict.
- `full` → spawn as normal.

Before generating the Go/No-Go recommendation, spawn `producer` via Task using gate **PR-MILESTONE** (`standards/director-gates.md`).

Pass: milestone name and target date, current completion percentage, blocked story count, velocity data from sprint reports (if available), list of cut candidates.

Present the producer's assessment inline within the Go/No-Go section. The producer's verdict (ON TRACK / AT RISK / OFF TRACK) informs the overall recommendation — do not issue a GO against an OFF TRACK producer verdict without explicit user acknowledgement.

---

## Phase 4: Save Review

Present the review to the user.

Ask: "May I write this to `production/milestones/[milestone-name]-review.md`?"

If yes, write the file, creating the directory if needed. Verdict: **COMPLETE** — milestone review saved.

When `memory_bank/` exists, propose the actual companion snapshot draft at
`memory_bank/t3_archive/sprint_snapshots/milestone-[name]-review-[YYYY-MM-DD].md`.
Write it only when that path/effect is covered by existing scoped authority or the
user approves the concrete report-and-snapshot changeset. Main review approval alone
does not authorize the companion; keep an uncovered snapshot pending while saving
the authorized milestone review.

Include milestone scope, verdict, completed deliverables, open risks, QA/release
links, and next gate recommendation. If `memory_bank/` does not exist, do not
create it from `/milestone-review`; keep the existing milestone review behavior
and say: "Run `/constitute` to establish the memory_bank governance control
plane."

If no, stop here. Verdict: **BLOCKED** — user declined write.

---

## Phase 5: Next Steps

- Run `/gate-check` for a formal phase gate verdict if this milestone marks a development phase boundary.
- Run `/sprint-plan` to adjust the next sprint based on the scope recommendations above.
