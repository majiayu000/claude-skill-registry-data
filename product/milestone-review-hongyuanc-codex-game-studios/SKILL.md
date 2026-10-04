---
name: milestone-review
description: "Use when a milestone checkpoint needs completeness, quality, risk, schedule, and go/no-go assessment."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Do not add unlisted files or behavior; pause and request a new approval if scope expands.

## Phase 0: Parse Arguments

Extract the milestone name (`current` or a specific name) and resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `.codex/studio.toml` and use its `review_mode` value
3. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. Never use a competing persistent setting

See `../../../.codex/docs/director-gates.md` for the full check pattern.

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

Before generating the Go/No-Go recommendation, spawn `producer` through Codex custom-agent delegation using gate **PR-MILESTONE** (`../../../.codex/docs/director-gates.md`).

Pass: milestone name and target date, current completion percentage, blocked story count, velocity data from sprint reports (if available), list of cut candidates.

Present the producer's assessment inline within the Go/No-Go section. The producer's verdict (ON TRACK / AT RISK / OFF TRACK) informs the overall recommendation.

If OFF TRACK, use `request_user_input` before generating the recommendation:
- Prompt: "Producer verdict: OFF TRACK. The milestone is in jeopardy. This review will recommend NO-GO. How do you want to proceed?"
- Options:
  - `[A] Accept NO-GO — generate the full review with that recommendation`
  - `[B] Override to CONDITIONAL GO — I'll document the accepted risks myself`
  - `[C] Stop — I want to address blockers before generating the review`

If AT RISK, use `request_user_input`:
- Prompt: "Producer verdict: AT RISK. Milestone may slip. How should the Go/No-Go section be framed?"
- Options:
  - `[A] CONDITIONAL GO — include producer's conditions in the review`
  - `[B] NO-GO — conditions cannot be met in time`
  - `[C] GO — I accept the risk and want to proceed`

Do not issue a GO against an OFF TRACK verdict unless the user explicitly selects [B] above.

---

## Phase 4: Save Review

Present the review to the user.

Ask: "May I write this to `production/milestones/[milestone-name]-review.md`?"

If yes, write the file, creating the directory if needed. Verdict: **COMPLETE** — milestone review saved.

If no, stop here. Verdict: **BLOCKED** — user declined write.

---

## Phase 5: Next Steps

- Run `$gate-check` for a formal phase gate verdict if this milestone marks a development phase boundary.
- Run `$sprint-plan` to adjust the next sprint based on the scope recommendations above.
