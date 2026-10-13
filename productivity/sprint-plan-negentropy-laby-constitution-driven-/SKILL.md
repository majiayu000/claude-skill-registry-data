---
name: sprint-plan
description: "Generates a new sprint plan or updates an existing one based on the current milestone, completed work, and available capacity. Pulls context from production documents and design backlogs."
argument-hint: "[new|update|status] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
context: |
  !ls production/sprints/ 2>/dev/null
---

## QA policy, facts and authority

Apply `standards/evidence-lifecycle.md`, `standards/notes-adr-sync.md` and existing
collaboration authority. Read actual `workflow/workflow-catalog.yaml`, domain,
current transition and established project QA scope, including initialized
`memory_bank/t1_axioms/qa_context.md` or the existing owning Story/plan/decision.
QA orchestration is optional by default; strict obligations need explicit source,
authority and exact checks/scope. Review mode does not select strict QA. Absent
optional Memory Bank/QA Context with no actual strict selection uses the catalog's
default optional orchestration; disclose absence without requiring initialization.
Unknown applies to unresolved actual required applicability or conflicting policy,
not optional context absence. Resolve that affected scope before dependent claims;
Honor actual user-specified per-effect approval conditions when determining coverage;
do not invent strict obligations or passing results.
Optional orchestration never waives required Story AC, governing DoD, decisions,
evidence or required review. Type tables are starting points; actual owners decide
requirements. Each required check retains PASS/FAIL/NotRun/Blocked/Pending; N/A
needs a governing applicability reason and cannot erase a failure.

Separate sufficiency, actual execution, independence, acceptance and completion.
Files/keywords/counts, planning cases and self-checks prove none of the other facts.
Read relied-on bodies and minimum required direct/indirect dependency closure;
retain full SHA-256/byte sizes, recoverable originals and original-path witnesses.
Disclose reading omissions. Exact bound historical results may be reused only
where selected workflow permits, labeled historical with original runtime/observer,
inputs and scope; never call them this run's execution. Missing required originals
or observations leave affected checks incomplete. Risk acceptance is a separate
scoped record; it cannot change FAIL/NotRun/Blocked/Pending to PASS or completion.

Reuse named paths/effects authority across roles/retries; before new authority show
draft and complete effect set, asking only for material new scope. Review-only
invokes no write entrypoint. Report-only writes its new report, excluding inputs,
indexes, session/sprint/stage state and closure. Existing report paths require a
new revision with prior evidence preserved; index effects need their own covered
scope and historical links. Optional Memory Bank absence uses Story/report/
conversation fallback without initialization, publication or activation.

## User Guide

- When to use: Generates a new sprint plan or updates an existing one based on the current milestone, completed work, and available capacity. Pulls context from production documents and design backlogs.
- Inputs: Command arguments: `/sprint-plan [new|update|status] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Parse Arguments

Parse the existing review flags and their values separately from the positional
base selector. Omitted positional selector defaults to `new`, including a legal
flag-only call such as `/sprint-plan --review full`. A supplied positional selector
must be exactly `new`, `update` or `status`. Any other non-flag selector stops before
context-dependent gates or writes: name the invalid selector and request correction,
without treating it as `new` or a legal review value. Do not reject a legal existing
review flag as a positional mode or invent a new CLI interface.

Resolve review mode once and store it for all applicable gate spawns this run:
1. If `--review` is present, require its nonempty value to be exactly
   `full`, `lean` or `solo`; use the valid explicit value.
2. Otherwise, if `production/review-mode.txt` exists, read and trim its value;
   require exactly `full`, `lean` or `solo`, then use that valid global value.
3. Only when both override and global file are absent default to `lean`.

Resolve once and reuse the same valid mode for all applicable director spawns.
Empty/invalid explicit values or an existing empty/invalid global file stop mode
resolution before any director spawn, gate-skip verdict or status/closure write.
Report the actual invalid source/value and request correction; do not silently
fall back to lean or invent a completed gate. Preserve existing legal CLI/modes.

See `standards/director-gates.md` for the full check pattern.

---

## Phase 1: Gather Context

0. **Domain detection**: Read concept bodies and apply actual domain/capability
   evidence under `standards/technical-preferences.md`. Missing concepts do not
   default Game; configured Product uses its applicable paths. Legacy Game
   compatibility requires actual configured engine/domain and Game behavior.
   Conflicting sources or absent evidence remain Unknown, blocking dependent
   domain routing/claims; independent neutral status/planning reports continue.
   No domain detection initializes Memory Bank or rewrites selectors/QA/gates.

1. **Read the current milestone** from `production/milestones/`.

2. **Read the previous sprint** (if any) from `production/sprints/` to
   understand velocity and carryover.

3. **Scan design documents** in `design/cdd/` for features tagged as ready
   for implementation.

4. **Check the risk register** at `production/risk-register/`.

---

## Phase 2: Generate Output

For `new`:

**Generate a sprint plan** following this format and present it to the user. Do NOT ask to write yet — the producer feasibility gate (Phase 4) runs first and may require revisions before the file is written.

```markdown
# Sprint [N] -- [Start Date] to [End Date]

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
- [ ] Required Story closure conditions pass; QA plan optional by default, required only under explicitly selected scope
- [ ] All Logic/Integration stories have passing unit/integration tests
- [ ] Selected required smoke/strict checks have adequate actual PASS evidence; optional follow-up remains separate
- [ ] Required selected QA sign-off actually qualifies with exact evidence/authority; optional `/team-qa` recommended when useful
- [ ] No S1 or S2 bugs in delivered features
- [ ] Design documents updated for any deviations
- [ ] Code reviewed and merged
```

For `status`:

**Generate a conversation-only status report**, then return from the skill. Do not enter later drafting, director gates, QA orchestration or file-write phases:

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

## Phase 3: Draft Sprint Status Projection

For `new`/`update`, prepare `production/sprint-status.yaml` in memory as a draft.
Do not write it or the sprint plan in Phase 3. Selected producer review and QA
scope handling (Phases 4 and 5) occur before the unified covered writes.
This is the machine-readable projection of actual Story state/closure — read by
`/sprint-status`, `/story-done`, and `/help` without markdown parsing.

Record the exact YAML path/create-or-update effect in the proposed changeset; reuse covered authority, or ask for missing/new authority at the final write step after Phases 4 and 5.

Format:

```yaml
# Auto-generated by /sprint-plan. Updated by /story-done.
# DO NOT edit manually — use /story-done to update story status.

sprint: [N]
goal: "[sprint goal]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

stories:
  - id: "[epic-story, e.g. 1-1]"
    name: "[story name]"
    file: "[production/epics/[epic-slug]/story-NNN-[slug].md]"
    priority: must-have        # must-have | should-have | nice-to-have
    status: ready-for-dev      # backlog | ready-for-dev | in-progress | review | done | blocked
    owner: ""
    estimate_days: 0
    blocker: ""
    completed: ""
```

Initialize each story from the sprint plan's task tables:
- Must Have tasks → `priority: must-have`; `ready-for-dev` only with actual current readiness, otherwise backlog/blocked as found
- Should Have tasks → `priority: should-have`, `status: backlog`
- Nice to Have tasks → `priority: nice-to-have`, `status: backlog`

For `update`, read YAML plus actual Story/closure inputs. Carry done only with exact eligible required PASS/review/authority binding; preserve blocked/unverified facts and actions. New/changed Stories need actual readiness, not priority-based assumptions. Dropping/removing rows is a separately named effect with historical evidence retained. `status` mode is read-only.

---

## Phase 4: Producer Feasibility Gate

**Review mode check** — apply before spawning PR-SPRINT:
- `solo` → skip. Note: "PR-SPRINT skipped — Solo mode." Proceed to Phase 5 (QA plan gate).
- `lean` → skip (not a PHASE-GATE). Note: "PR-SPRINT skipped — Lean mode." Proceed to Phase 5 (QA plan gate).
- `full` → spawn as normal.

Before finalising the sprint plan, spawn `producer` via Task using gate **PR-SPRINT** (`standards/director-gates.md`).

Pass: proposed story list (titles, estimates, dependencies), total team capacity in hours/days, any carryover from the previous sprint, milestone constraints and deadline.

Present the producer's assessment. If UNREALISTIC, revise the story selection (defer stories to Should Have or Nice to Have) before asking for write approval. If CONCERNS, surface them and let the user decide whether to adjust.

After handling the actual producer verdict (or legal mode skip), continue to Phase 5 before writing either sprint plan or YAML. Director approval/skip does not grant write or QA qualification authority.

Include this guidance in the final draft/output:

> **Scope check:** If this sprint includes stories added beyond the original epic scope, run `/scope-check [epic]` to detect scope creep before implementation begins.

---

## Phase 5: QA Scope and Plan Follow-Up

Read actual catalog/domain/current phase and explicitly selected strict QA scope.
Find a plan for exact active sprint/Story scope; latest mtime/keywords do not prove
applicability. Default optional QA: absence is a recommendation, not an implementation
or phase blocker; required Story AC/DoD/evidence remains binding. Selected required
plan/sign-off: record actual source/authority/scope/checks and Pending/NotRun/Blocked.
Missing obligation prevents dependent qualification, while independent planning can
continue. Unknown required applicability needs resolution before claiming readiness;
optional QA Context absence with no actual strict selection follows catalog default optional orchestration; it implies neither strict obligations nor passing execution.

Offer `/qa-plan sprint` if useful. Plan/warning writes need covered named effects.
Planning operation COMPLETE means authorized plan saved, not sprint/Story/QA complete.

### Final Covered Writes (new/update only)

After required producer review/decision and QA-scope handling, present the final
plan and optional YAML projection with their exact named paths/effects. Reuse
existing covered authorization; ask once only for missing/materially new effects,
e.g. "May I write this sprint plan to `production/sprints/sprint-[N].md` and the
named `production/sprint-status.yaml` projection?" Apply each covered effect and
preserve any unsupported/blocked actual state. Plan-only authority excludes YAML.
If writing is declined, report BLOCKED for that write; conversation drafting may
still finish. COMPLETE reports only successfully authorized plan work, with actual
QA/closure facts unchanged. `status` mode returned earlier and never reaches here.


---

## Phase 6: Next Steps

After the sprint plan is written and QA plan status is resolved:

- `/qa-plan sprint` — optional default planning aid; required only under explicitly selected scope, while Story required AC/evidence retains its actual owner
- `/story-readiness [story-file]` — validate a story is ready before starting it
- `/dev-story [story-file]` — begin implementing the first story
- `/sprint-status` — check progress mid-sprint
- `/scope-check [epic]` — verify no scope creep before implementation begins
