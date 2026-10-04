---
name: sprint-plan
description: "Use when a sprint needs creation, replanning, capacity allocation, milestone alignment, or backlog prioritization."
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

### Native readiness gate for `$codex-game-studios:team-qa`

Before invoking or routing to `$codex-game-studios:team-qa`, confirm that `team-qa` is present in the current task's available skill catalog. If unavailable, report
`Staged dependency: $codex-game-studios:team-qa is not available`, defer the handoff, do not invoke `$codex-game-studios:team-qa`, do not route to `$codex-game-studios:team-qa`, and do not search for or copy a repository-local skill file.

## Phase 0: Parse Arguments

Extract the mode argument (`new`, `update`, or `status`) and resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `.codex/studio.toml` and use its `review_mode` value
3. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. Never use a competing persistent setting

See `../../../.codex/docs/director-gates.md` for the full check pattern.

**Review mode check**: `.codex/studio.toml` is the single persistent source. A
`--review` value is in-memory for this run only and is never written.

---

## Phase 1: Gather Context

1. **Read the current milestone** from `production/milestones/`.

2. **Read the previous sprint** (if any) from `production/sprints/` to
   understand velocity and carryover.

3. **Scan design documents** in `design/gdd/` for features tagged as ready
   for implementation.

4. **Check the risk register** at `production/risk-register/`.

---

## Phase 2: Generate Output

For `new`:

**Generate a sprint plan** following this format and present it to the user. Do NOT ask to write yet — the producer feasibility gate (Phase 4) runs first and may require revisions before the file is written.

```markdown
# Sprint [N] — [Start Date] to [End Date]

## Sprint Goal
[One sentence describing what this sprint achieves toward the milestone]

## Capacity
- Total days: [X]
- Buffer (20%): [Y days reserved for unplanned work]
- Available: [Z days]

## Tasks

### Must Have (Critical Path)
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Should Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Nice to Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

## Carryover from Previous Sprint
| Task | Reason | New Estimate |
|------|--------|-------------|

## Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|

## Dependencies on External Factors
- [List any external dependencies]

## Definition of Done for this Sprint
- [ ] All Must Have tasks completed
- [ ] All tasks pass acceptance criteria
- [ ] QA plan exists (`production/qa/qa-plan-sprint-[N].md`)
- [ ] All Logic/Integration stories have passing unit/integration tests
- [ ] Smoke check passed (`$codex-game-studios:smoke-check sprint`)
- [ ] QA sign-off report: APPROVED or APPROVED WITH CONDITIONS (`$codex-game-studios:team-qa sprint`)
- [ ] No S1 or S2 bugs in delivered features
- [ ] Design documents updated for any deviations
- [ ] Code reviewed and merged
```

For `update`:

**Update an existing sprint plan**:

1. Read the most recent sprint plan from `production/sprints/`.
2. Present the current story list with their current statuses from `production/sprint-status.yaml`.
3. Ask the user what to change: stories to add, remove, reprioritize, or re-estimate. Use `request_user_input` to gather changes.
4. Apply the changes and re-present the full revised plan for review.
5. Re-run the producer feasibility gate (Phase 4) on the revised plan.
6. Prepare the updated markdown plan and yaml together, then continue through the producer and QA gates before requesting approval.

Note: `update` mode does not reset story statuses. Stories already marked `in-progress` or `done` keep their status. Only `backlog` and `ready-for-dev` stories can be removed or reprioritized freely.

For `status`:

**Generate a status report**:

```markdown
# Sprint [N] Status -- [Date]

## Progress: [X/Y tasks complete] ([Z%])

### Completed
| Task | Completed By | Notes |
|------|-------------|-------|

### In Progress
| Task | Owner | % Done | Blockers |
|------|-------|--------|----------|

### Not Started
| Task | Owner | At Risk? | Notes |
|------|-------|----------|-------|

### Blocked
| Task | Blocker | Owner of Blocker | ETA |
|------|---------|-----------------|-----|

## Burndown Assessment
[On track / Behind / Ahead]
[If behind: What is being cut or deferred]

## Emerging Risks
- [Any new risks identified this sprint]
```

---

## Phase 3: Prepare Sprint Status File

After generating a new sprint plan, also prepare the `production/sprint-status.yaml` content.
This is the machine-readable source of truth for story status — read by
`$codex-game-studios:sprint-status`, `$codex-game-studios:story-done`, and `$codex-game-studios:help` without markdown parsing.

**Do not write the yaml yet** — hold it in context. The producer feasibility gate (Phase 4) may revise the story list. Both files will be written together after Phase 4 in a single write approval.

Format:

```yaml
# Auto-generated by $codex-game-studios:sprint-plan. Updated by $codex-game-studios:story-done and $codex-game-studios:dev-story.
# DO NOT edit manually — use $codex-game-studios:story-done to update story status.
#
# Status value mapping (yaml ↔ story file Status field):
#   backlog        ↔  Not Started
#   ready-for-dev  ↔  Ready
#   in-progress    ↔  In Progress
#   review         ↔  In Review
#   done           ↔  Complete
#   blocked        ↔  Blocked

sprint: [N]
goal: "[sprint goal]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

stories:
  - id: "[epic-story, e.g. 1-1]"
    name: "[story name]"
    file: "[production/stories/path.md]"
    priority: must-have        # must-have | should-have | nice-to-have
    status: ready-for-dev      # backlog | ready-for-dev | in-progress | review | done | blocked
    owner: ""
    estimate_days: 0
    blocker: ""
    completed: ""
```

Initialize each story from the sprint plan's task tables:
- Must Have tasks → `priority: must-have`, `status: ready-for-dev`
- Should Have tasks → `priority: should-have`, `status: backlog`
- Nice to Have tasks → `priority: nice-to-have`, `status: backlog`

For `update`: read the existing `sprint-status.yaml`, carry over statuses for
stories that haven't changed, add new stories, remove dropped ones.

---

## Phase 4: Producer Feasibility Gate

**Review mode check** — apply before spawning PR-SPRINT:
- `solo` → skip. Note: "PR-SPRINT skipped — Solo mode." Proceed to Phase 5 (QA plan gate).
- `lean` → skip (not a PHASE-GATE). Note: "PR-SPRINT skipped — Lean mode." Proceed to Phase 5 (QA plan gate).
- `full` → spawn as normal.

Before finalising the sprint plan, spawn `producer` through Codex custom-agent delegation using gate **PR-SPRINT** (`../../../.codex/docs/director-gates.md`).

Pass: proposed story list (titles, estimates, dependencies), total team capacity in hours/days, any carryover from the previous sprint, milestone constraints and deadline.

Present the producer's assessment.

If UNREALISTIC: revise the story selection (defer stories to Should Have or Nice to Have) and re-present the updated plan before asking for write approval.

If CONCERNS, use `request_user_input`:
- Prompt: "Producer flagged concerns with this sprint plan. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the risk`
  - `[B] Adjust scope — defer some Should Have stories`
  - `[C] Extend the sprint timeline`

If [A]: continue to the QA plan gate without writing.
If [B]: revise the story list, re-present the updated plan, then continue to the QA plan gate without writing.
If [C]: adjust sprint dates and capacity, re-present the updated plan, then continue to the QA plan gate without writing.

Do not write any sprint artifact after the producer gate. The QA plan gate may still revise the draft.

Include this note in the draft when applicable:

> **Scope check:** If this sprint includes stories added beyond the original epic scope, run `$codex-game-studios:scope-check [epic]` to detect scope creep before implementation begins.

---

## Phase 5: QA Plan Gate

The workflow must pass the current in-memory sprint draft and exact story scope directly to
`$codex-game-studios:qa-plan sprint-draft`. Do not ask `$codex-game-studios:qa-plan` to discover a persisted sprint and
never let it select the prior or most recently modified sprint. Receive the QA
plan as an in-memory draft; neither workflow writes yet.

If QA planning identifies untestable criteria, missing evidence paths, or scope
gaps, revise the in-memory sprint draft and QA plan together, then re-run the
producer assessment if capacity or scope changed. If a complete QA plan cannot
be produced, report BLOCKED and write no sprint artifact.

## Complete Proposed Changeset Approval

After the producer and QA gates are fully resolved, show one complete proposed changeset containing:

- `production/sprints/sprint-[N].md`
- `production/sprint-status.yaml`
- `production/qa/qa-plan-sprint-[N]-[date].md`
- every file affected by QA-gate revisions, or an explicit statement that QA-gate revisions only changed the listed sprint draft

This is one combined complete changeset for the sprint plan, sprint status, QA plan, and any approved index/status updates. Show the final content or precise summary for every listed path, then ask once for approval. Write nothing before this approval. If the producer response, QA status, scope, dates, story list, or path list changes afterward, present a revised complete changeset and obtain a new approval before writing. After approval, write only the listed files and report Verdict: **COMPLETE**. If approval is declined, write nothing and report Verdict: **BLOCKED**.

---

## Phase 6: Next Steps

After the complete changeset is approved, written, and QA plan status is resolved:

- The combined QA plan is already written with the sprint; do not regenerate it from another sprint.
- `$codex-game-studios:story-readiness [story-file]` — validate a story is ready before starting it
- `$codex-game-studios:dev-story [story-file]` — begin implementing the first story
- `$codex-game-studios:sprint-status` — check progress mid-sprint
- `$codex-game-studios:scope-check [epic]` — verify no scope creep before implementation begins

**Review mode configuration:** All director gates respect `.codex/studio.toml`.
The canonical `review_mode = "phase-gated"` maps to lean optional-review depth
while mandatory director gates still run. A per-run
`--review full|lean|solo` override is not persisted.
