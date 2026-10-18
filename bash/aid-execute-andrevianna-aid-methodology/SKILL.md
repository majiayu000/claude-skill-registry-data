---
name: aid-execute
description: >
  Carry out one planned task and review the result. Use this skill when tasks have been
  detailed and you are ready for the work to actually be done. It runs the task according to
  its type -- RESEARCH, DESIGN, IMPLEMENT, TEST, DOCUMENT, MIGRATE, REFACTOR or CONFIGURE --
  then loops through review and fixes until the result meets the configured minimum grade.
  Each delivery runs on its own branch, so deliveries stay isolated from each other.
allowed-tools: Read Glob Grep Write Edit Bash Shell Terminal
argument-hint: "work-001 (required if multiple works)  task-001 (required)"
---

# Execute Task

Read the type. Do the work. Review it. Fix it. Ship it.

## ⚠️⚠️ MANDATORY: write task State AS IT CHANGES -- read this first

> **Whoever executes this task -- the main/orchestrator agent running it
> DIRECTLY, or a dispatched sub-agent -- MUST write the task's `State` field
> the instant it changes: `In Progress` before starting work, `In Review`
> before dispatching the reviewer, and a terminal value (`Done` / `Failed`)
> when finished. No agent may skip, batch, or defer these writes, on the
> flat OR full layout, whether this task is run alone or as part of a pool
> dispatch.** The full mandate, the exact command for each transition, and the
> why lives in `references/state-execute.md § MANDATORY: State-Write
> Protocol` -- read it before Step 1 below. Skipping these writes is the
> single most common root cause of a task that shows `Pending` in the
> dashboard for its entire execution and then jumps straight to `Done`.

## ⚠️ Pre-flight Checks

### Check 1: Locate Work and Task

1. Read first arg: if it starts with `work-` → use that work directory; if it starts with `task-` → treat as shorthand (single-work auto-select below)
2. If work arg not provided (or shorthand): enumerate works **cross-worktree**: run
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git
   worktree; never the local `.aid/works/` glob, which is empty on `master`), taking
   each record's field-1 `work_id` — single record → auto-select; multiple records →
   list them, ask user to choose; zero records on any worktree → **STOP.** "No works
   found. Run `/aid-describe` first."
3. Read second arg (or first arg when shorthand): the `task-NNN` identifier; also resolve `delivery-NNN` from the task identifier or from the Source field

   **Locate + enter the work's worktree.** Now that the work id is resolved (steps 1-3 above) and
   **before** step 4 below reads anything under `.aid/works/{work}/…`, follow
   `.aid/runtime/templates/downstream-worktree-entry.md` to normalize the work id to its bare
   `work-NNN` branch name, `locate` the worktree (which **always exits 0** and returns
   `<path>\t<status>`), and enter the returned path. Keep the defensive empty-path/non-zero
   backstop that stops rather than operate blindly — it should not fire against the real helper.
   Never create a new worktree — creation belongs to the work-starting skills only.
4. **Detect the layout** (per-work, DECLARED first; additive — does not change the full-path resolution below). Read `pipeline.path` from the work-root `STATE.yml`: `lite` → flat, `full` → nested. Infer from file presence ONLY when no value is declared, which means an un-migrated work:
   - **Full path (nested):** `.aid/works/{work}/deliveries/` exists → tasks live at `deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`.
   - **Flat path (feature-001, single-delivery):** `.aid/works/{work}/tasks/task-NNN/DETAIL.md` exists directly under the work root AND no `deliveries/` wrapper under it → the delivery is always the synthesized `delivery-001` (no per-task `STATE.yml`; task mutable cells live in the work-root `STATE.yml`'s `tasks_lifecycle` mapping instead — see `## Workspace` below).
5. Find the task definition at the layout-appropriate path from step 4.
6. Task not found → **STOP.** List available tasks.

### Check 2: Read Task

Read the task definition from:
- **Full path:** `.aid/works/{work}/deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`
- **Flat path:** `.aid/works/{work}/tasks/task-NNN/DETAIL.md`

It has 6 sections:
- **Title** — what this task does
- **Type** — RESEARCH | DESIGN | IMPLEMENT | TEST | DOCUMENT | MIGRATE | REFACTOR | CONFIGURE
- **Source** — `work-NNN-{name} → delivery-NNN` (which work and delivery)
- **Depends on** — which tasks must be complete before this one (or `—` for none)
- **Scope** — what to produce or modify (files, tests, docs, configs — depends on type)
- **Acceptance Criteria** — concrete, testable conditions

### Check 2b: Verify Dependencies Met

Read the Execution Graph:
- **Full path:** from PLAN.md's `#### Execution Graph` block for this task's delivery.
- **Flat path:** from the work-root `PLAN.md`'s top-level `## Execution Graph` (see
  `references/state-execute.md § Locate the Execution Graph`).

Check that all tasks listed in `Depends on:` have `State: Done`:
- **Full path:** in their respective `deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`
  files (the top-level `state` key).
- **Flat path:** in the work-root `STATE.yml`'s `tasks_lifecycle` mapping (keyed by `task-NNN`).

If any dependency is not Done → **STOP.** List which dependencies are pending.

### Check 3: Read Minimum Grade

Run `bash .aid/runtime/scripts/config/read-setting.sh --skill execute --key minimum_grade --default A` to resolve the minimum grade for this skill (`.aid/settings.yml` is the source).
This is the exit criterion for the review loop.

### Check 4: Verify Not in Plan Mode

- ✅ `Default` or `Auto-accept edits` → Proceed.
- ❌ `Plan mode` → **STOP.**

### Check 5: Branch Isolation

**One branch per delivery. All tasks in a delivery share the same branch.**

1. Extract `delivery-NNN` from the task's Source field (flat path: always the
   synthesized `delivery-001`, carried by the task's `Source: ... -> delivery-001`
   field — no `deliveries/` folder to derive it from, so this step needs no change)
2. Branch name: `aid/{work}-delivery-NNN` (e.g., `aid/{work}-delivery-001`)
3. **Look up the project's VCS** from `infrastructure.md § Source Control` (via INDEX.md)
   to determine the correct branch/commit commands.

| Situation | Action |
|-----------|--------|
| Branch doesn't exist | Create it from current HEAD using VCS branch command |
| Branch exists, not checked out | Switch to it |
| Branch exists, already checked out | Continue |

⚠️ **Before creating a new branch:** verify working tree is clean.
If dirty → **STOP.** Ask user to commit or stash first.

**Exception:** RESEARCH and DOCUMENT tasks may not need a branch (no code changes).
If the task only produces `.aid/` artifacts, skip branch isolation.

### Check 6: Determine State

Read the task's `State`:
- **Full path:** from `deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`'s top-level `state` key, if the file exists.
- **Flat path:** from the work-root `STATE.yml`'s `tasks_lifecycle` entry for `task-NNN`, if present.

Apply the routing table in `## State Detection` below.

Print the state-entry line and "you are here" map:

**EXECUTE:**
```
[State: EXECUTE] — Running the executor agent to produce task deliverables.
aid-execute  ▸ you are here
  [● EXECUTE ] → [ REVIEW ] → [ FIX ] → [ DONE ]
                 ↑__________________|
```

**REVIEW:**
```
[State: REVIEW] — Grading task output against acceptance criteria with a clean-context reviewer.
aid-execute  ▸ you are here
  [✓ EXECUTE ] → [● REVIEW ] → [ FIX ] → [ DONE ]
                 ↑___________________|
```

**FIX:**
```
[State: FIX] — Applying CODE-issue fixes and returning to REVIEW.
aid-execute  ▸ you are here
  [✓ EXECUTE ] → [✓ REVIEW ] → [● FIX ] → [ DONE ]
                 ↑____________________|
```

**DONE:**
```
[State: DONE] — Grade meets minimum; task complete.
aid-execute  ▸ you are here
  [✓ EXECUTE ] → [✓ REVIEW ] → [✓ FIX ] → [● DONE ]
```

## State Detection

State detection reads the files on disk, every run; nothing inferred from conversation
history counts as state. Read the task's `State` from
`deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`'s top-level `state` key (full path) —
or, on the flat path, the work-root `STATE.yml`'s `tasks_lifecycle` entry for `task-NNN`:

| Condition | State |
|-----------|-------|
| File absent or `State: _none yet_` | **EXECUTE** (Step 1) |
| `State: In Progress`, no issues pending | **EXECUTE** (Step 1 — resume) |
| `State: In Review`, issues listed | **FIX** (Step 3) |
| `State: Done` | **RE-RUN** (see Re-run below) |

## Inputs

**KB via INDEX.md** — Read `.aid/knowledge/INDEX.md`. Use summaries to decide which
KB docs are relevant to this task, then load them. Let the INDEX guide you.

**Always load (not KB):**
- Task definition — primary prompt:
  - Full path: `.aid/works/{work}/deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`
  - Flat path: `.aid/works/{work}/tasks/task-NNN/DETAIL.md`
- Task mutable state (State, Review, Elapsed, Notes):
  - Full path: `.aid/works/{work}/deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`
  - Flat path: work-root `.aid/works/{work}/STATE.yml`'s `tasks_lifecycle` entry for `task-NNN`
  - **The requirements SLICE this task traces to — not the whole document:**

    ```
    bash .aid/runtime/scripts/execute/slice-requirements.sh .aid/works/{work} task-NNN
    ```

    Prints the task's own `§ 11` feature section (the technical specification it builds
    against), the `§ 9` `AC-N` entries its `**Source:**` line cites, and the identity
    block. Nothing else.

    Every task execution loads a statement of intent; when that statement is the whole
    of `REQUIREMENTS.md`, a 16-task work reads the whole document 16 times, and the cost
    scales with task count where a gate's does not. On this repo's own requirements the
    slice is ~93% smaller than the document.

    The slice is derivable because the task already declares what it traces to — no new
    field, no map to maintain, no judgment at read time. A task whose `**Source:**` cites
    no criterion exits 3 rather than returning a near-empty slice: it has nothing to be
    judged against, which is a defect in the DETAIL, not a small slice.

    Read the whole document only when the task genuinely spans the work — rare, and
    visible as a `**Source:**` citing many criteria rather than as a judgment call here.
- `.aid/works/{work}/PLAN.md` — delivery context and **Execution Graph** (dependencies and parallelism;
  flat path: the top-level `## Execution Graph`, single delivery)

**Load if exists:**
- `.aid/works/{work}/known-issues.md` — issues in code the task touches

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| EXECUTE | `references/state-execute.md` | _(type-specific — see state file; delivery-mode uses pool dispatch PD-0→PD-6)_ | → REVIEW |
| REVIEW | `references/state-review.md` | `aid-reviewer` (Small tier, quick-check only — no grade loop per FR2) | → DONE |
| FIX | `references/state-fix.md` | _(same type as EXECUTE)_ | → REVIEW |
| DONE | _(inline — task complete)_ | `inline` | → halt |
| RE-RUN | `references/state-re-run.md` | `inline` | → halt |
| DELIVERY-GATE | `references/state-delivery-gate.md` | `aid-reviewer` (tier = complexity score) | → halt (grade ≥ min) / → FIX (grade < min) |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

## Dispatch Protocol

This skill follows the L1+L2+L3 subagent-visibility protocol (heartbeats, ETA timers,
calibration). The full checklist lives in
`.aid/runtime/templates/dispatch-protocol-checklist.md`; read it before any subagent
dispatch in this skill.

## Workspace

```
.aid/
  knowledge/                ← shared KB (via INDEX.md)
    STATE.md                ← Q&A, Review History (settings -> .aid/settings.yml)
  works/
    work-NNN-{name}/
      STATE.yml                ← work-level pipeline header (AUTHORED); derived views (read-only)
      REQUIREMENTS.md         ← work definition; § 11 holds the feature sections
      PLAN.md                 ← delivery stanzas (each the delivery definition) +
                              #  execution graph
      known-issues.md         ← issues to watch for
      deliveries/
        delivery-NNN/
          STATE.yml              ← delivery lifecycle (SD-8, AUTHORED) + gate + Q&A + derived task rollup
          tasks/
            task-NNN/
              DETAIL.md         ← PRIMARY INPUT (task definition: Type, Scope, AC)
              STATE.yml          ← task mutable state: state, review, elapsed, notes
      REQUIREMENTS.md        ← § 11 `### Feature NNN` sections: architectural
                             #  constraints (full path only)
```

**Flat (single-delivery) layout — feature-001.** Detected by `pipeline.path: lite`
in the work-root `STATE.yml`; for an un-migrated work that declares nothing, inferred
from `tasks/task-NNN/DETAIL.md` present directly under the work root AND no
`deliveries/` wrapper under it. Additive alongside the full path above (AC-9 — no
regression):

```
.aid/
  works/
    work-NNN-{name}/                     (flat / single-delivery — no features/, no deliveries/)
      STATE.yml                ← work-level pipeline header (AUTHORED) + the promoted
                                 delivery_lifecycle (tasks_lifecycle) /
                                 delivery_gate AUTHORED keys (single writer;
                                 replaces delivery-NNN/STATE.yml + per-task STATE.yml)
      REQUIREMENTS.md          ← requirements AND, in § 11, the single feature section
                                 with its own #### Technical Specification
      PLAN.md                  ← the single delivery: its Deliverables stanza, which IS
                                 the delivery definition (objective, scope, Gate
                                 Criteria), plus the top-level ## Execution Graph
                                 (no ### delivery-NNN heading)
      tasks/
        task-NNN/
          DETAIL.md            ← PRIMARY INPUT (task definition: Type, Scope, AC);
                                 NO per-task STATE.yml — cells live in the work
                                 STATE.yml's tasks_lifecycle mapping instead
```

Branch is synthesized `aid/{work}-delivery-001` (Check 5); delivery gate criteria
come from the delivery's stanza in `PLAN.md` (see
`references/state-delivery-gate.md`).

**Ephemeral worktrees (pool dispatch PD-2):** `.aid/.worktrees/task-NNN/` are
temporary git worktrees provisioned for parallel pool dispatch. They are on the
shared delivery branch and are removed after the task completes (PD-4 step 5).
They are distinct from the PERSISTENT worktrees the dashboard discovers (Pillar 4
— `git worktree list`). Do not confuse the two: the ephemeral worktrees are an
execution-isolation mechanism; the persistent worktrees are a user-registered
parallel-branch mechanism visible to the dashboard.

**Nesting with the work-level worktree:** Check 1 step 3's locate+enter paragraph above already
entered this work's persistent worktree before any of the above runs, so these per-task ephemeral
worktrees are provisioned **nested, unchanged, inside** that entered work-level worktree —
different root (`.aid/.worktrees/task-NNN/` vs. the work-level worktree root that `worktree-lifecycle.sh root` prints),
different branch, different purpose; the two compose without conflict
(`.aid/runtime/templates/downstream-worktree-entry.md § Composition with aid-execute's per-task
worktrees`).

## Delivery Lifecycle

Execution follows the **Execution Graph** in PLAN.md. Tasks run in dependency order.
Independent tasks (listed in the "Can Be Done In Parallel" table) can run concurrently.

```
create branch aid/{work}-delivery-001
  → /aid-execute work-001 task-001 [RESEARCH]      ← investigate → review → ✅
  → /aid-execute work-001 task-002 [DESIGN]        ← mockup → review → ✅
  → /aid-execute work-001 task-003 [IMPLEMENT]  ┐
  → /aid-execute work-001 task-004 [IMPLEMENT]  ┘  ← parallel (both depend on task-002)
  → /aid-execute work-001 task-005 [TEST]          ← waits for task-003 + task-004
  → /aid-execute work-001 task-006 [DOCUMENT]      ← ADR → review → ✅
  → merge to main
```

All tasks in a delivery accumulate on the same branch.
RESEARCH and DOCUMENT tasks that produce only `.aid/` artifacts may skip branching.

**Delivery-mode pool dispatch (FR6):** When `/aid-execute` is invoked for a
delivery (not a single task), a continuous pool dispatcher replaces the serial
loop. Full pool dispatch spec — including the `run_in_background` capability
probe and graceful degradation — lives in
`references/state-execute.md § EXECUTE-WAVE: Pool Dispatch (PD-0 through PD-6)`.

**Graceful degradation:** On hosts where the Agent tool's `run_in_background`
parameter is not supported, `aid-execute` detects this via a capability probe
(PD-0 step 2 in `references/state-execute.md`) and automatically falls back to
effective `MaxConcurrent=1`. A user-visible notice is printed:

```
[degradation] MaxConcurrent={N} requested, host capability=sequential — running effective=1
```

The degradation event has no per-task home to log to (it fires once, before any task is
dispatched, so there is no `task-NNN` `dispatch_log` entry it belongs to; the retired
`## Calibration Log` markdown section that could take a non-task row directly no
longer has a corresponding key — `work-state-template.yml`'s Calibration Log/Dispatches
views are DERIVED solely from per-task `dispatch_log` entries). The degradation notice
above is therefore the sole record of this event. The pool algorithm runs identically
at pool size 1 — no behavioral difference other than one task in flight at a time
(sequential execution).

### EXECUTE-WAVE: AC4 Sub-unit Drill-down

When executing a delivery wave, render a sub-unit snapshot after each sub-unit transition.

> **Authoritative spec:** `references/state-execute-drilldown.md`
> contains the full snapshot format, status-icon vocabulary, re-render trigger
> rules (1-second coalescing), serial-task fallback semantics, and failure
> tolerance. This SKILL.md section is a brief router-level pointer; do not
> duplicate the spec here — read it from state-execute-drilldown.md so the two
> stay in sync.

## Impediments

If the agent encounters something it can't resolve:

**MANDATORY, before writing the IMPEDIMENT file -- per `references/state-execute.md § MANDATORY: State-Write Protocol`:**
update the task's own State to `Failed`, whether this task is being executed
by the main/orchestrator agent directly or by a dispatched sub-agent. Do NOT
leave the task showing `In Progress`/`In Review` while an unresolved
impediment sits unaddressed -- that is exactly the "invisible/misleading task"
state the protocol exists to prevent:
```bash
bash .aid/runtime/scripts/execute/writeback-state.sh \
    --delivery-id DDD --task-id NNN --field State --value "Failed"
```

```markdown
# Impediment — task-NNN

**Type:** wrong-assumption | missing-dependency | architecture-conflict | kb-gap
**Description:** What happened and why the agent stopped
**Options:**
1. {Option A} — trade-offs
2. {Option B} — trade-offs
**Recommendation:** Option {N} because {reason}
```

Write to `.aid/works/{work}/IMPEDIMENT-task-NNN.md`.

Resolution by type:
- **kb-gap** → targeted `/aid-discover` → update KB → retry
- **architecture-conflict** → `/aid-specify` for the feature
- **missing-dependency** → `/aid-detail` (might need another task first)
- **wrong-assumption** → update task or SPEC, retry

After resolving: delete IMPEDIMENT file; write task State back to `In Progress`
(the same mandatory write as Step 1's EXECUTE entry — this is a fresh entry
into EXECUTE, not a continuation that can skip it); retry from Step 1.

## Output

- Artifacts appropriate to the task type (code, tests, docs, configs, research, designs)
- Grade >= minimum grade (from `bash .aid/runtime/scripts/config/read-setting.sh --skill execute --key minimum_grade --default A`)
- Commit messages reference task-NNN (for types that produce commits)
- `deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`'s `state`/`review` keys updated with full review history
  (flat path: the work-root `STATE.yml`'s `tasks_lifecycle` entry for `task-NNN`)
- `deliveries/delivery-NNN/STATE.yml`'s `delivery_state` advanced (Executing -> Gated -> Done, or Blocked)
  (flat path: the work-root `STATE.yml`'s `delivery_state`)
- IMPEDIMENT-task-NNN.md if blocked

## Ticket Suggestion (conditional)

If a catalogued `issue-tracker` connector exists in `.aid/connectors/` → print a suggestion:
consider updating the corresponding ticket's status via `/aid-update-ticket status` (e.g. In
Progress → Done) and, if a loopback occurred, recording context via `/aid-update-ticket
comment`. Optional, user-initiated, never auto-invoked; silent (no output) if no issue-tracker
connector is catalogued.

## Quality Checklist

- [ ] Task Type read correctly from `deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`
  (flat path: `tasks/task-NNN/DETAIL.md` directly under the work root)
- [ ] Task State read from `deliveries/delivery-NNN/tasks/task-NNN/STATE.yml` (not the work-level rollup)
  (flat path: the work-root `STATE.yml`'s `tasks_lifecycle` entry — not the plural Tasks State derived view)
- [ ] On correct delivery branch (or skipped for RESEARCH/DOCUMENT-only tasks)
- [ ] KB docs loaded via INDEX.md (not hardcoded)
- [ ] Type-specific rules followed
- [ ] Acceptance criteria from task all met
- [ ] Scope boundary respected (no extra work)
- [ ] Reviewer graded using deterministic rubric (separate agent, clean context)
- [ ] Reviewer did NOT fix anything — only graded and listed issues
- [ ] ALL issues presented to user (not just CODE)
- [ ] Non-CODE issues marked as Loopback with target phase
- [ ] No silent workarounds — impediments documented
- [ ] Commit messages reference task-NNN (where applicable)
- [ ] `deliveries/delivery-NNN/tasks/task-NNN/STATE.yml`'s `state`/`review` keys have full review history
  (flat path: the work-root `STATE.yml`'s `tasks_lifecycle` entry)
- [ ] `deliveries/delivery-NNN/STATE.yml`'s `delivery_state` advanced to correct enum value (SD-8)
  (flat path: the work-root `STATE.yml`'s `delivery_state`)
